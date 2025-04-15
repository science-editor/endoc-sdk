import pytest
from endoc.services.single_paper_search import SinglePaperSearchService
from endoc.models.single_paper import SinglePaperData
from endoc.queries import SINGLE_PAPER_QUERY

def test_single_paper_success(mock_api_client, mock_single_paper_response):
    """Test SinglePaperSearchService.get_single_paper with successful response."""
    _, mocker = mock_api_client
    mocker.post(
        "https://endoc.ethz.ch/graphql",
        additional_matcher=lambda req: "singlePaper" in req.text,
        json=mock_single_paper_response
    )
    
    service = SinglePaperSearchService(api_key="fake-api-key")
    result = service.get_single_paper(id_value="221802394")
    
    assert isinstance(result, SinglePaperData)
    assert result.status == "SUCCESS"
    assert result.message == "Paper retrieved"
    assert result.response.id_int == 221802394
    assert result.response.Title == "Sample Paper"
    assert result.response.Author[0].FamilyName == "Doe"
    assert result.response.Reference[0].Title == "Referenced Paper"

def test_single_paper_empty(mock_api_client, mock_single_paper_empty_response):
    """Test SinglePaperSearchService.get_single_paper with empty response."""
    _, mocker = mock_api_client
    mocker.post(
        "https://endoc.ethz.ch/graphql",
        additional_matcher=lambda req: "singlePaper" in req.text,
        json=mock_single_paper_empty_response
    )
    
    service = SinglePaperSearchService(api_key="fake-api-key")
    result = service.get_single_paper(id_value="221802394")
    
    assert isinstance(result, SinglePaperData)
    assert result.status == "SUCCESS"
    assert result.message == "No paper found"
    assert result.response is None

def test_single_paper_invalid_response(mock_api_client):
    """Test SinglePaperSearchService.get_single_paper with invalid response."""
    _, mocker = mock_api_client
    mocker.post(
        "https://endoc.ethz.ch/graphql",
        additional_matcher=lambda req: "singlePaper" in req.text,
        json={"data": {}}  # Missing 'singlePaper' key
    )
    
    service = SinglePaperSearchService(api_key="fake-api-key")
    with pytest.raises(ValueError, match="No 'singlePaper' key found in response."):
        service.get_single_paper(id_value="221802394")