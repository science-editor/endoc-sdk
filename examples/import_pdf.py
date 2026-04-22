"""
Example: Import PDFs into Endoc and display the results.

Usage (from endoc-sdk root):

    # Single file
    python examples/import_pdf.py --path Papers/thesis.pdf

    # Multiple files
    python examples/import_pdf.py --paths Papers/a.pdf Papers/b.pdf

    # Entire folder
    python examples/import_pdf.py --folder Papers/

    # Folder with subfolders
    python examples/import_pdf.py --folder Papers/ --recursive

    # Include matched references (not just your uploads)
    python examples/import_pdf.py --path Papers/thesis.pdf --include-references
"""

import argparse
import os
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

load_dotenv(ROOT / ".env", override=True)

from endoc import EndocClient  # noqa: E402


def print_paper(paper, index: int) -> None:
    authors = ", ".join(
        f"{a.GivenName} {a.FamilyName}" for a in paper.authors
    )
    print(f"\n  [{index}] {paper.title or '(untitled)'}")
    print(f"      Collection: {paper.collection}  ID: {paper.id_value}")
    print(f"      Authors:    {authors or '(none)'}")
    print(f"      Year: {paper.year or 'N/A'}  Venue: {paper.venue or 'N/A'}  DOI: {paper.doi or 'N/A'}")

    if paper.abstract:
        wrapped = textwrap.fill(paper.abstract[:300], 64)
        print(f"      Abstract:   {wrapped.replace(chr(10), chr(10) + '                  ')}")
        if len(paper.abstract) > 300:
            print("                  ...")

    if paper.sections:
        print(f"      Sections:   {len(paper.sections)} parsed sections")

    if paper.references:
        print(f"      References: {len(paper.references)} extracted")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Import PDFs into Endoc via the SDK."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--path", help="Path to a single PDF file.")
    group.add_argument("--paths", nargs="+", help="Paths to multiple PDF files.")
    group.add_argument("--folder", help="Path to a folder of PDFs.")

    parser.add_argument(
        "--api-key",
        default=os.getenv("ENDOC_API_KEY") or os.getenv("API_KEY"),
        help="Endoc API key (defaults to ENDOC_API_KEY env var).",
    )
    parser.add_argument("--recursive", action="store_true", help="Scan subfolders.")
    parser.add_argument("--batch-size", type=int, default=10, help="Batch size.")
    parser.add_argument("--max-file-mb", type=int, default=50, help="Max file size (MB).")
    parser.add_argument(
        "--include-references",
        action="store_true",
        help="Include matched reference papers, not just your uploads.",
    )
    args = parser.parse_args()

    if not args.api_key:
        sys.exit("ERROR: No API key. Set ENDOC_API_KEY in .env or pass --api-key.")

    client = EndocClient(api_key=args.api_key)

    # ── Build the import_pdf() call ─────────────────────────────────────
    kwargs = {
        "recursive": args.recursive,
        "batch_size": args.batch_size,
        "max_file_mb": args.max_file_mb,
        "include_references": args.include_references,
    }

    if args.path:
        kwargs["path"] = args.path
        print(f"Uploading: {args.path}")
    elif args.paths:
        kwargs["paths"] = args.paths
        print(f"Uploading {len(args.paths)} file(s)")
    else:
        kwargs["folder"] = args.folder
        print(f"Uploading folder: {args.folder} (recursive={args.recursive})")

    # ── Import ──────────────────────────────────────────────────────────
    result = client.import_pdf(**kwargs)

    print(f"\nStatus:  {result.status}")
    print(f"Message: {result.message}")
    print(f"Papers:  {len(result.papers)}")

    if not result.papers:
        print("\nNo papers returned.")
        return

    for i, paper in enumerate(result.papers, 1):
        print_paper(paper, i)

    print()


if __name__ == "__main__":
    main()
