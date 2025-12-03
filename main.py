from __future__ import annotations

import os
import json
import time
from typing import Any, Dict, Iterable, List, Optional, Tuple, Set

from dotenv import load_dotenv
from pyzotero import zotero

from endoc import EndocClient, AuthenticationError, PermissionError, RateLimitError, APIError


# --------------------------- Utils ---------------------------

def chunked(seq: List[Any], n: int) -> Iterable[List[Any]]:
    for i in range(0, len(seq), n):
        yield seq[i:i+n]


def getenv_required(name: str) -> str:
    val = os.getenv(name)
    if not val:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return val


# ----------------------- Zotero helpers ----------------------

def make_zotero_client() -> zotero.Zotero:
    """
    Env:
      ZOTERO_API_KEY
      ZOTERO_LIBRARY_ID
      ZOTERO_LIBRARY_TYPE ('user' or 'group'; default 'user')
    """
    api_key = getenv_required("ZOTERO_API_KEY")
    library_id = getenv_required("ZOTERO_LIBRARY_ID")
    library_type = (os.getenv("ZOTERO_LIBRARY_TYPE") or "user").lower()
    if library_type not in {"user", "group"}:
        raise RuntimeError("ZOTERO_LIBRARY_TYPE must be 'user' or 'group'.")
    return zotero.Zotero(library_id, library_type, api_key)


def fetch_collections(z: zotero.Zotero) -> List[Dict[str, Any]]:
    return z.everything(z.collections())


def build_collection_maps(collections: List[Dict[str, Any]]):
    by_key = {c["key"]: c for c in collections}
    children: Dict[str, List[str]] = {}
    for c in collections:
        parent = c.get("data", {}).get("parentCollection")
        if parent:
            children.setdefault(parent, []).append(c["key"])
    return by_key, children


def name_of(c: Dict[str, Any]) -> str:
    return (c.get("data", {}) or {}).get("name", "").strip()


def path_for(c: Dict[str, Any], by_key: Dict[str, Dict[str, Any]]) -> str:
    parts = [name_of(c)]
    parent = c.get("data", {}).get("parentCollection")
    while parent:
        pc = by_key.get(parent)
        if not pc:
            break
        parts.append(name_of(pc))
        parent = pc.get("data", {}).get("parentCollection")
    return " / ".join(reversed([p for p in parts if p]))


def build_collection_paths(collections: List[Dict[str, Any]]) -> List[Tuple[str, str]]:
    by_key, _ = build_collection_maps(collections)
    rows: List[Tuple[str, str]] = []
    for c in collections:
        p = path_for(c, by_key)
        if p:
            rows.append((c["key"], p))
    rows.sort(key=lambda kv: kv[1].lower())
    return rows


def prompt_select_collection(paths: List[Tuple[str, str]]) -> Optional[Tuple[str, str]]:
    """
    Returns (key, path) or None if cancelled.
    """
    if not paths:
        print("No collections found in this Zotero library.")
        return None

    print("\n📁 Zotero Collections")
    for i, (_, path) in enumerate(paths, start=1):
        print(f"  {i:>2}. {path}")
    print("  0. Cancel")

    while True:
        raw = input("\nSelect a collection by number: ").strip()
        if not raw.isdigit():
            print("Please enter a valid number.")
            continue
        choice = int(raw)
        if choice == 0:
            return None
        if 1 <= choice <= len(paths):
            key, path = paths[choice - 1]
            return key, path
        print(f"Choose a number between 0 and {len(paths)}.")


def descendant_keys(root_key: str, children: Dict[str, List[str]]) -> List[str]:
    out: List[str] = []
    stack = [root_key]
    seen: Set[str] = {root_key}
    while stack:
        k = stack.pop()
        for child in children.get(k, []):
            if child not in seen:
                out.append(child)
                seen.add(child)
                stack.append(child)
    return out


def fetch_items_in_collection_top(z: zotero.Zotero, collection_key: str) -> List[Dict[str, Any]]:
    """
    Top-level (parent) items only. We DON'T pass itemType filters to the API,
    then we filter attachments/notes client-side to avoid 400s.
    """
    return z.everything(z.collection_items_top(collection_key))


def fetch_items_in_collection_recursive_top(
    z: zotero.Zotero,
    root_key: str,
    children: Dict[str, List[str]],
) -> List[Dict[str, Any]]:
    """
    Top-level items from root and all descendant subcollections.
    De-duplicates by Zotero item key.
    """
    all_keys = [root_key] + descendant_keys(root_key, children)
    items: List[Dict[str, Any]] = []
    seen_item_keys: Set[str] = set()
    for k in all_keys:
        for it in z.everything(z.collection_items_top(k)):
            ik = it.get("key")
            if ik and ik not in seen_item_keys:
                items.append(it)
                seen_item_keys.add(ik)
    return items


def filter_parent_biblio_items(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Keep only parent bibliographic items (drop attachments and notes).
    """
    keep: List[Dict[str, Any]] = []
    dropped = 0
    for it in items:
        typ = (it.get("data") or {}).get("itemType")
        if typ in {"attachment", "note"}:
            dropped += 1
            continue
        keep.append(it)
    if dropped:
        print(f"   (filtered out {dropped} attachment/note items)")
    return keep


def extract_title(item: Dict[str, Any]) -> str:
    return (item.get("data", {}).get("title") or "").strip()


# ----------------------- Endoc helpers ----------------------

def make_endoc_client() -> EndocClient:
    api_key = (
        os.getenv("ENDOC_API_KEY")
        or os.getenv("API_KEY")
        or os.getenv("PROD_API_KEY")
        or None
    )
    return EndocClient(api_key=api_key)


def endoc_title_search(
    client: EndocClient,
    titles: List[str],
    *,
    batch_size: int = 25,
    sleep_secs: float = 0.2,
) -> Dict[str, Dict[str, Any]]:
    """
    Returns mapping: title -> {found, collection, id_field, id_type, id_value}
    """
    out: Dict[str, Dict[str, Any]] = {}
    for batch in chunked(titles, batch_size):
        time.sleep(sleep_secs)
        try:
            res = client.title_search(batch)
        except RateLimitError:
            time.sleep(2.0)
            res = client.title_search(batch)
        for item in (res.response or []):
            out[item.Title] = {
                "found": item.found,
                "collection": getattr(item, "collection", None),
                "id_field": getattr(item, "id_field", None),
                "id_type": getattr(item, "id_type", None),
                "id_value": getattr(item, "id_value", None),
            }
    return out


# -------------------------- Main ----------------------------

def main() -> int:
    load_dotenv()

    # 1) List collections and pick one
    try:
        z = make_zotero_client()
        collections = fetch_collections(z)
        paths = build_collection_paths(collections)
        selected = prompt_select_collection(paths)
        if not selected:
            print("Cancelled.")
            return 0
        selected_key, selected_path = selected
        by_key, children = build_collection_maps(collections)
        print(f"\n✅ Selected collection: {selected_path}  (key: {selected_key})")
    except Exception as e:
        print(f"❌ Failed to fetch collections: {e}")
        return 1

    # 2) Fetch top-level items, optionally including subcollections
    recursive = (os.getenv("ZOTERO_RECURSIVE", "0").strip().lower() in {"1", "true", "yes"})
    print(f"   Recursive fetch of subcollections: {'ON' if recursive else 'OFF'}")

    try:
        if recursive:
            items = fetch_items_in_collection_recursive_top(z, selected_key, children)
        else:
            items = fetch_items_in_collection_top(z, selected_key)
    except Exception as e:
        print(f"❌ Failed to fetch items from collection: {e}")
        return 1

    # Filter out attachments/notes client-side
    items = filter_parent_biblio_items(items)

    titles = [t for t in (extract_title(it) for it in items) if t]
    seen, unique_titles = set(), []
    for t in titles:
        if t not in seen:
            seen.add(t)
            unique_titles.append(t)

    print(f"   Found {len(items)} parent items; {len(unique_titles)} unique titled items.")
    for t in unique_titles[:5]:
        print(f"   • {t}")
    if not unique_titles:
        print("ℹ️  No titled items in this collection.")
        return 0

    # 3) Match in Endoc
    print(f"\n🔎 Resolving {len(unique_titles)} unique titles in Endoc…")
    try:
        client = make_endoc_client()
        mapping = endoc_title_search(client, unique_titles)
    except AuthenticationError as e:
        print(f"❌ Endoc authentication failed: {e}")
        return 1
    except PermissionError as e:
        print(f"❌ Endoc permission error: {e}")
        return 1
    except APIError as e:
        print(f"❌ Endoc API error: {e}")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {type(e).__name__}: {e}")
        return 1

    matched = sum(1 for t in unique_titles if mapping.get(t, {}).get("found"))
    print("\n📄 Results:")
    for t in unique_titles:
        m = mapping.get(t, {})
        if m.get("found"):
            print(f"  ✓ {t}  [{m.get('collection')}:{m.get('id_value')}]")
        else:
            print(f"  ✗ {t}  (not found)")

    print(f"\n✅ Matched {matched}/{len(unique_titles)} titles in: {selected_path}")

    # 4) Save JSON
    out_path = os.getenv("OUTPUT_JSON", "zotero_collection_endoc_mapping.json")
    payload = {
        "collection_key": selected_key,
        "collection_path": selected_path,
        "recursive": recursive,
        "total_items_parent_only": len(items),
        "unique_titles": len(unique_titles),
        "matched": matched,
        "records": [
            {
                "title": t,
                **mapping.get(t, {"found": False, "collection": None, "id_field": None, "id_type": None, "id_value": None}),
            }
            for t in unique_titles
        ],
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(f"💾 Wrote mapping to {out_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())