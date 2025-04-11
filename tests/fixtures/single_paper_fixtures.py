import pytest
from endoc.models.single_paper import SinglePaperData, SinglePaperResponseBody, SinglePaperContent, Author, PublicationDate, PaperReference, PaperID

@pytest.fixture
def mock_single_paper_response():
    """Sample response for single_paper wrapped in 'data'."""
    return {
        "data": {
            "singlePaper": {
                "status": "SUCCESS",
                "message": "Paper retrieved",
                "response": {
                    "_id": "paper_123",
                    "id_int": 221802394,
                    "DOI": "10.1000/test.doi",
                    "Title": "Sample Paper",
                    "Content": {
                        "Abstract": "Sample abstract.",
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
                        ],
                        "Fullbody_Parsed": [],
                        "Fullbody": "Sample full text."
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
                    "Reference": [
                        {
                            "Title": "Referenced Paper",
                            "Author": [{"FamilyName": "Smith", "GivenName": "Jane"}],
                            "Venue": "Another Journal",
                            "PublicationDate": {"Year": 2022, "Month": 1, "Day": None, "Name": None},
                            "ReferenceText": "Smith et al., 2022",
                            "PaperID": None  # Changed to None
                        }
                    ]
                }
            }
        }
    }

@pytest.fixture
def mock_single_paper_empty_response():
    """Sample response with no paper found wrapped in 'data'."""
    return {
        "data": {
            "singlePaper": {
                "status": "SUCCESS",
                "message": "No paper found",
                "response": None
            }
        }
    }