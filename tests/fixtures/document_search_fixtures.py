import pytest

@pytest.fixture
def mock_document_search_response():
    """Sample response for document_search wrapped in 'data'."""
    return {
        "data": {
            "documentSearch": {
                "status": "SUCCESS",
                "message": "Search completed",
                "response": {
                    "search_stats": {
                        "DurationTotalSearch": 0.123,
                        "nMatchingDocuments": "10"
                    },
                    "paper_list": [
                        {
                            "collection": "S2AG",
                            "id_field": "id_int",
                            "id_type": "int",
                            "id_value": "221802394"
                        }
                    ],
                    "reranking_scores": [0.95, 0.87],
                    "prefetching_scores": [0.91, 0.83]
                }
            }
        }
    }

@pytest.fixture
def mock_document_search_empty_response():
    """Sample response with no results wrapped in 'data'."""
    return {
        "data": {
            "documentSearch": {
                "status": "SUCCESS",
                "message": "No matching documents",
                "response": None
            }
        }
    }