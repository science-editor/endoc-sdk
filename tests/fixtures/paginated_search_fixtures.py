import pytest
from endoc.models.paginated_search import PaginatedSearchData, PaginatedSearchResponseBody, Content, AbstractParsedItem, Author, PublicationDate

@pytest.fixture
def mock_paginated_search_response():
    """Sample response for paginated_search wrapped in 'data'."""
    return {
        "data": {
            "paginatedSearch": {
                "status": "SUCCESS",
                "message": "Search completed",
                "response": [
                    {
                        "_id": "paper_123",
                        "DOI": "10.1000/test.doi",
                        "Title": "Sample Paper",
                        "Content": {
                            "Abstract": "This is a sample abstract.",
                            "Abstract_Parsed": [
                                {
                                    "section_id": "abs1",
                                    "section_title": "Abstract",
                                    "section_text": [
                                        {
                                            "paragraph_id": "p1",
                                            "paragraph_text": [
                                                {
                                                    "sentence_id": "s1",
                                                    "sentence_text": "This is a sample sentence.",
                                                    "sentence_similarity": 0.95,
                                                    "cite_spans": []
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        "Author": [
                            {"FamilyName": "Doe", "GivenName": "John"}
                        ],
                        "Venue": "Sample Journal",
                        "PublicationDate": {
                            "Year": 2023,
                            "Month": 5,
                            "Day": None,
                            "Name": None
                        },
                        "id_int": 221802394,
                        "relevant_sentences": ["This is a sample sentence."]
                    }
                ]
            }
        }
    }

@pytest.fixture
def mock_paginated_search_empty_response():
    """Sample response with no results wrapped in 'data'."""
    return {
        "data": {
            "paginatedSearch": {
                "status": "SUCCESS",
                "message": "No matching documents",
                "response": []
            }
        }
    }