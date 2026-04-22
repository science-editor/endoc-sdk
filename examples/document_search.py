"""
Example: Search for papers using document_search.

Usage:
    python examples/document_search.py
    python examples/document_search.py --ranking-variable BERT --keywords "machine learning"
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
    parser = argparse.ArgumentParser(description="Search documents on Endoc.")
    parser.add_argument("--api-key", default=os.getenv("ENDOC_API_KEY"))
    parser.add_argument("--ranking-variable", default="BERT")
    parser.add_argument("--keywords", nargs="*", default=["AvailableField:Content.Fullbody_Parsed"])
    args = parser.parse_args()

    if not args.api_key:
        sys.exit("Set ENDOC_API_KEY in .env or pass --api-key.")

    client = EndocClient(api_key=args.api_key)
    result = client.document_search(
        ranking_variable=args.ranking_variable,
        keywords=args.keywords,
    )

    print(f"Status: {result.status}")

    if result.response and result.response.search_stats:
        stats = result.response.search_stats
        print(f"Matching documents: {stats.nMatchingDocuments}")
        print(f"Search duration:    {stats.DurationTotalSearch}")

    if result.response and result.response.paper_list:
        print(f"\nTop results ({len(result.response.paper_list)} papers):")
        for i, paper in enumerate(result.response.paper_list[:5], 1):
            print(f"  {i}. {paper.collection}/{paper.id_value} ({paper.id_type})")
    else:
        print("No papers found.")


if __name__ == "__main__":
    main()
