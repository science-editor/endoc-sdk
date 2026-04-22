"""
Example: Summarize a paper.

Usage:
    python examples/summarize_paper.py --id 204744049
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
    parser = argparse.ArgumentParser(description="Summarize a paper on Endoc.")
    parser.add_argument("--api-key", default=os.getenv("ENDOC_API_KEY"))
    parser.add_argument("--id", required=True, help="Paper id_value.")
    args = parser.parse_args()

    if not args.api_key:
        sys.exit("Set ENDOC_API_KEY in .env or pass --api-key.")

    client = EndocClient(api_key=args.api_key)
    result = client.summarize(id_value=args.id)

    print(f"Status: {result.status}")
    print(f"Message: {result.message}")

    if not result.response:
        print("No summary returned.")
        return

    print(f"Summary sentences: {len(result.response)}")
    for sentence in result.response[:10]:
        tag = sentence.tag if hasattr(sentence, "tag") else ""
        text = sentence.sentence_text if hasattr(sentence, "sentence_text") else str(sentence)
        print(f"  [{tag}] {text[:120]}{'...' if len(text) > 120 else ''}")

    if len(result.response) > 10:
        print(f"  ... and {len(result.response) - 10} more")


if __name__ == "__main__":
    main()
