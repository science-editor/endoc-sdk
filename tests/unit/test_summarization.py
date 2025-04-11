import pytest
from endoc.services.summarization import SummarizationService
from endoc.models.summarization import SummarizationResponseData
from endoc.queries import SUMMARIZE_PAPER_QUERY

def test_summarization_success(mock_api_client, mock_summarization_response):
    """Test SummarizationService.summarize_paper with successful response."""
    _, mocker = mock_api_client
    mocker.post(
        "https://endoc.ethz.ch/graphql",
        additional_matcher=lambda req: "summarizePaper" in req.text,
        json=mock_summarization_response
    )
    
    service = SummarizationService(api_key="fake-api-key")
    result = service.summarize_paper(id_value="221802394")
    
    assert isinstance(result, SummarizationResponseData)
    assert result.status == "SUCCESS"
    assert result.message == "Summarization completed"
    assert len(result.response) == 2
    assert result.response[0].sentence_text == "This is a summarized sentence."
    assert result.response[1].tag == "neutral"

def test_summarization_empty(mock_api_client, mock_summarization_empty_response):
    """Test SummarizationService.summarize_paper with empty response."""
    _, mocker = mock_api_client
    mocker.post(
        "https://endoc.ethz.ch/graphql",
        additional_matcher=lambda req: "summarizePaper" in req.text,
        json=mock_summarization_empty_response
    )
    
    service = SummarizationService(api_key="fake-api-key")
    result = service.summarize_paper(id_value="221802394")
    
    assert isinstance(result, SummarizationResponseData)
    assert result.status == "SUCCESS"
    assert result.message == "No summarization available"
    assert result.response == []

def test_summarization_invalid_response(mock_api_client):
    """Test SummarizationService.summarize_paper with invalid response."""
    _, mocker = mock_api_client
    mocker.post(
        "https://endoc.ethz.ch/graphql",
        additional_matcher=lambda req: "summarizePaper" in req.text,
        json={"data": {}}  # Missing 'summarizePaper' key
    )
    
    service = SummarizationService(api_key="fake-api-key")
    with pytest.raises(ValueError, match="No 'summarizePaper' key found in response."):
        service.summarize_paper(id_value="221802394")