from endoc.services.document_search import DocumentSearchService
from endoc.models.document_search import DocumentSearchData

def test_document_search_success(mock_api_client, mock_document_search_response):
    _, mocker = mock_api_client
    mocker.post(
        "https://endoc.ethz.ch/graphql",
        additional_matcher=lambda req: "documentSearch" in req.text,
        json=mock_document_search_response
    )
    
    service = DocumentSearchService(api_key="fake-api-key")
    result = service.search_documents(ranking_variable="BERT", keywords=["test"])
    
    assert isinstance(result, DocumentSearchData)
    assert result.status == "SUCCESS"
    assert result.response.search_stats.nMatchingDocuments == "10"
    assert len(result.response.paper_list) == 1
    assert result.response.paper_list[0].id_value == "221802394"

def test_document_search_empty(mock_api_client, mock_document_search_empty_response):
    _, mocker = mock_api_client
    mocker.post(
        "https://endoc.ethz.ch/graphql",
        additional_matcher=lambda req: "documentSearch" in req.text,
        json=mock_document_search_empty_response
    )
    
    service = DocumentSearchService(api_key="fake-api-key")
    result = service.search_documents(ranking_variable="BERT", keywords=["test"])
    
    assert isinstance(result, DocumentSearchData)
    assert result.status == "SUCCESS"
    assert result.message == "No matching documents"
    assert result.response is None