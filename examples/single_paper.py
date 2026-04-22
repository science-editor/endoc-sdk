"""
Example: Retrieve a single paper by its ID.

Usage:
    python examples/single_paper.py --id 204744049
    python examples/single_paper.py --id 1001 --collection UserUploaded
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
    parser = argparse.ArgumentParser(description="Retrieve a single paper from Endoc.")
    parser.add_argument("--api-key", default=os.getenv("ENDOC_API_KEY"))
    parser.add_argument("--id", required=True, help="Paper id_value.")
    parser.add_argument("--collection", default="S2AG")
    parser.add_argument("--id-field", default="id_int")
    parser.add_argument("--id-type", default="int")
    args = parser.parse_args()

    if not args.api_key:
        sys.exit("Set ENDOC_API_KEY in .env or pass --api-key.")

    client = EndocClient(api_key=args.api_key)
    result = client.single_paper(
        id_value=args.id,
        collection=args.collection,
        id_field=args.id_field,
        id_type=args.id_type,
    )

    print(f"Status: {result.status}")

    if not result.response:
        print("No paper found.")
        return

    r = result.response
    authors = ", ".join(f"{a.GivenName} {a.FamilyName}" for a in (r.Author or []))

    print(f"Title:   {r.Title}")
    print(f"Authors: {authors or '(none)'}")
    print(f"Venue:   {r.Venue or 'N/A'}")
    print(f"Year:    {r.PublicationDate.Year if r.PublicationDate else 'N/A'}")
    print(f"DOI:     {r.DOI or 'N/A'}")

    if r.Content and r.Content.Abstract:
        print(f"Abstract: {r.Content.Abstract[:300]}{'...' if len(r.Content.Abstract) > 300 else ''}")

    if r.Content and r.Content.Fullbody_Parsed:
        print(f"Sections: {len(r.Content.Fullbody_Parsed)}")

    if r.Reference:
        print(f"References: {len(r.Reference)}")


if __name__ == "__main__":
    main()
