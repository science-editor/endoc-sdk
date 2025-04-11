from endoc.models.document_search import DocumentSearchData, DocumentSearchResponseBody

def test_document_search_model(mock_document_search_response):
    data = mock_document_search_response["data"]["documentSearch"]
    result = DocumentSearchData(**data)
    assert result.status == "SUCCESS"
    assert isinstance(result.response, DocumentSearchResponseBody)
    assert result.response.search_stats.DurationTotalSearch == 0.123

def test_document_search_model_empty(mock_document_search_empty_response):
    data = mock_document_search_empty_response["data"]["documentSearch"]
    result = DocumentSearchData(**data)
    assert result.status == "SUCCESS"
    assert result.message == "No matching documents"
    assert result.response is None