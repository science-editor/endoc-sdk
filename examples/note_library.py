"""
Example: Retrieve a note's paper library.

Usage:
    python examples/note_library.py --note-id 69df555985fca6001a03e352
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
    parser = argparse.ArgumentParser(description="Get a note's paper library from Endoc.")
    parser.add_argument("--api-key", default=os.getenv("ENDOC_API_KEY"))
    parser.add_argument("--note-id", required=True, help="Note document ID.")
    args = parser.parse_args()

    if not args.api_key:
        sys.exit("Set ENDOC_API_KEY in .env or pass --api-key.")

    client = EndocClient(api_key=args.api_key)
    result = client.get_note_library(doc_id=args.note_id)

    print(f"Status: {result.status}")
    print(f"Message: {result.message}")

    if not result.response:
        print("No papers in library.")
        return

    print(f"Papers in library: {len(result.response)}")
    for i, paper in enumerate(result.response, 1):
        print(f"  {i}. {paper.id_collection}/{paper.id_value} ({paper.id_type})")


if __name__ == "__main__":
    main()
