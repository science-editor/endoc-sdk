import pytest
from endoc.services.paginated_search import PaginatedSearchService
from endoc.models.paginated_search import PaginatedSearchData
from endoc.queries import PAGINATED_SEARCH_QUERY

def test_paginated_search_success(mock_api_client, mock_paginated_search_response):
    """Test PaginatedSearchService.paginated_search with successful response."""
    _, mocker = mock_api_client
    mocker.post(
        "https://endoc.ethz.ch/graphql",
        additional_matcher=lambda req: "paginatedSearch" in req.text,
        json=mock_paginated_search_response
    )
    
    service = PaginatedSearchService(api_key="fake-api-key")
    paper_list = [
        {"collection": "S2AG", "id_field": "id_int", "id_type": "int", "id_value": "221802394"}
    ]
    result = service.paginated_search(paper_list=paper_list, keywords=["test"])
    
    assert isinstance(result, PaginatedSearchData)
    assert result.status == "SUCCESS"
    assert result.message == "Search completed"
    assert len(result.response) == 1
    assert result.response[0].id_int == 221802394
    assert result.response[0].Title == "Sample Paper"
    assert result.response[0].Author[0].FamilyName == "Doe"

def test_paginated_search_empty(mock_api_client, mock_paginated_search_empty_response):
    """Test PaginatedSearchService.paginated_search with empty response."""
    _, mocker = mock_api_client
    mocker.post(
        "https://endoc.ethz.ch/graphql",
        additional_matcher=lambda req: "paginatedSearch" in req.text,
        json=mock_paginated_search_empty_response
    )
    
    service = PaginatedSearchService(api_key="fake-api-key")
    paper_list = [
        {"collection": "S2AG", "id_field": "id_int", "id_type": "int", "id_value": "221802394"}
    ]
    result = service.paginated_search(paper_list=paper_list, keywords=["test"])
    
    assert isinstance(result, PaginatedSearchData)
    assert result.status == "SUCCESS"
    assert result.message == "No matching documents"
    assert result.response == []

def test_paginated_search_invalid_response(mock_api_client):
    """Test PaginatedSearchService.paginated_search with invalid response."""
    _, mocker = mock_api_client
    mocker.post(
        "https://endoc.ethz.ch/graphql",
        additional_matcher=lambda req: "paginatedSearch" in req.text,
        json={"data": {}}  # Missing 'paginatedSearch' key
    )
    
    service = PaginatedSearchService(api_key="fake-api-key")
    paper_list = [
        {"collection": "S2AG", "id_field": "id_int", "id_type": "int", "id_value": "221802394"}
    ]
    with pytest.raises(ValueError, match="No 'paginatedSearch' key found in response."):
        service.paginated_search(paper_list=paper_list)