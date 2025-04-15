#!/usr/bin/env python
import os
import json
from dotenv import load_dotenv
from endoc import EndocClient, register_service

# 1) Load environment variables
# Make sure you have a .env file in your project root:
#   API_KEY=your_api_key_here
load_dotenv()
api_key = os.getenv("PROD_API_KEY")

# 2) Instantiate the Endoc client
client = EndocClient(api_key)

# 3) Demonstrate Document Search
def demo_document_search():
    print("\n=== Document Search ===")
    doc_search_result = client.document_search(
        ranking_variable="BERT",
        keywords=["AvailableField:Content.Fullbody_Parsed"]
    )
    # Convert to dict for pretty printing
    doc_search_dict = doc_search_result.model_dump() if hasattr(doc_search_result, "model_dump") else doc_search_result
    print(json.dumps(doc_search_dict, indent=4))

# 4) Demonstrate Summarize Paper
def demo_summarize_paper():
    print("\n=== Summarize Paper ===")
    # Replace with a valid paper ID if needed
    summarize_result = client.summarize("221802394")
    summarize_dict = summarize_result.model_dump() if hasattr(summarize_result, "model_dump") else summarize_result
    print(json.dumps(summarize_dict, indent=4))

# 5) Demonstrate Paginated Search
def demo_paginated_search():
    print("\n=== Paginated Search ===")
    # Replace with a valid paper reference
    example_paper = {
        "collection": "S2AG",
        "id_field": "id_int",
        "id_type": "int",
        "id_value": "221802394"
    }
    paper_list = [example_paper]
    paginated_result = client.paginated_search(paper_list=paper_list)
    paginated_dict = paginated_result.model_dump() if hasattr(paginated_result, "model_dump") else paginated_result
    print(json.dumps(paginated_dict, indent=4))

# 6) Demonstrate Single Paper
def demo_single_paper():
    print("\n=== Single Paper ===")
    # Replace with a valid paper ID if needed
    single_paper_result = client.single_paper("221802394")
    single_paper_dict = single_paper_result.model_dump() if hasattr(single_paper_result, "model_dump") else single_paper_result
    print(json.dumps(single_paper_dict, indent=4))

# 7) Demonstrate Note Library
def demo_note_library():
    print("\n=== Get Note Library ===")
    # Replace with a valid note ID
    note_id = "679a1e2e5b25cf001a7c7157"
    note_library_result = client.get_note_library(note_id)
    note_library_dict = note_library_result.model_dump() if hasattr(note_library_result, "model_dump") else note_library_result
    print(json.dumps(note_library_dict, indent=4))

# 8) Demonstrate Custom Service
@register_service("combined_search")
def combined_search(self, paper_list, id_value):
    """
    A custom service that calls paginated_search and single_paper.
    You can define any composite logic here.
    """
    paginated = self.paginated_search(paper_list, keywords=["example"])
    single = self.single_paper(id_value)
    return {"paginated": paginated, "single": single}

def demo_custom_service():
    print("\n=== Custom Service (combined_search) ===")
    example_paper = {
        "collection": "S2AG",
        "id_field": "id_int",
        "id_type": "int",
        "id_value": "221802394"
    }
    paper_list = [example_paper]
    combined_result = client.combined_search(paper_list, "221802394")
    # Convert sub-results to dict for printing
    combined_dict = {
        "paginated": combined_result["paginated"].model_dump() if hasattr(combined_result["paginated"], "model_dump") else combined_result["paginated"],
        "single": combined_result["single"].model_dump() if hasattr(combined_result["single"], "model_dump") else combined_result["single"]
    }
    print(json.dumps(combined_dict, indent=4))

def main():
    if not api_key:
        print("Error: API_KEY not found in environment. Please set it in .env or your environment variables.")
        return

    # Uncomment the demos you want to run:
    demo_document_search()
    # demo_summarize_paper()
    # demo_paginated_search()
    # demo_single_paper()
    # demo_note_library()
    # demo_custom_service()

if __name__ == "__main__":
    main()