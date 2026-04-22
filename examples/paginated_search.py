"""
Example: Run a paginated search with highlighting.

Usage:
    python examples/paginated_search.py --id 204744049 --collection S2AG
"""

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env", override=True)

from endoc import EndocClient


def main() -> None:
    parser = argparse.ArgumentParser(description="Paginated search on Endoc.")
    parser.add_argument("--api-key", default=os.getenv("ENDOC_API_KEY"))
    parser.add_argument("--id", required=True, help="Paper id_value.")
    parser.add_argument("--collection", default="S2AG")
    parser.add_argument("--id-field", default="id_int")
    parser.add_argument("--id-type", default="int")
    parser.add_argument("--keywords", nargs="*", default=None)
    args = parser.parse_args()

    if not args.api_key:
        sys.exit("Set ENDOC_API_KEY in .env or pass --api-key.")

    client = EndocClient(api_key=args.api_key)
    result = client.paginated_search(
        paper_list=[{
            "collection": args.collection,
            "id_field": args.id_field,
            "id_type": args.id_type,
            "id_value": args.id,
        }],
        keywords=args.keywords,
    )

    print(f"Status: {result.status}")
    print(f"Papers returned: {len(result.response or [])}")

    if result.response:
        for i, paper in enumerate(result.response[:3], 1):
            print(f"\n  [{i}] {paper.Title}")
            authors = ", ".join(f"{a.GivenName} {a.FamilyName}" for a in (paper.Author or []))
            print(f"      Authors: {authors or '(none)'}")
            if paper.relevant_sentences:
                print(f"      Relevant sentences: {len(paper.relevant_sentences)}")


if __name__ == "__main__":
    main()
