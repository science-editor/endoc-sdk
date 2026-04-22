"""
Example: Search for papers by title.

Usage:
    python examples/title_search.py --titles "Attention Is All You Need"
    python examples/title_search.py --titles "Attention Is All You Need" "BERT: Pre-training"
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
    parser = argparse.ArgumentParser(description="Search papers by title on Endoc.")
    parser.add_argument("--api-key", default=os.getenv("ENDOC_API_KEY"))
    parser.add_argument("--titles", nargs="+", required=True, help="Paper titles to search for.")
    args = parser.parse_args()

    if not args.api_key:
        sys.exit("Set ENDOC_API_KEY in .env or pass --api-key.")

    client = EndocClient(api_key=args.api_key)
    result = client.title_search(titles=args.titles)

    print(f"Status: {result.status}")

    if not result.response:
        print("No results.")
        return

    for i, paper in enumerate(result.response, 1):
        found = "FOUND" if paper.found else "NOT FOUND"
        authors = ", ".join(f"{a.GivenName} {a.FamilyName}" for a in (paper.Author or []))
        print(f"\n  [{i}] {paper.Title} [{found}]")
        if paper.found:
            print(f"      Collection: {paper.collection}/{paper.id_value}")
            if authors:
                print(f"      Authors: {authors}")


if __name__ == "__main__":
    main()
