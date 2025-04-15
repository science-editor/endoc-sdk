import pytest
from endoc.models.summarization import SummarizationResponseData, SummarizationItem

@pytest.fixture
def mock_summarization_response():
    """Sample response for summarize_paper wrapped in 'data'."""
    return {
        "data": {
            "summarizePaper": {
                "status": "SUCCESS",
                "message": "Summarization completed",
                "response": [
                    {
                        "paragraph_id": "p1",
                        "section_id": "s1",
                        "sentence_id": "sent1",
                        "sentence_text": "This is a summarized sentence.",
                        "tag": "positive"
                    },
                    {
                        "paragraph_id": "p2",
                        "section_id": "s2",
                        "sentence_id": "sent2",
                        "sentence_text": "Another key point from the paper.",
                        "tag": "neutral"
                    }
                ]
            }
        }
    }

@pytest.fixture
def mock_summarization_empty_response():
    """Sample response with no summarization items wrapped in 'data'."""
    return {
        "data": {
            "summarizePaper": {
                "status": "SUCCESS",
                "message": "No summarization available",
                "response": []
            }
        }
    }