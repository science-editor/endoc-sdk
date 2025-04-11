from endoc import EndocClient

def test_endoc_client_document_search(mock_api_client, mock_document_search_response):
    api_client, mocker = mock_api_client
    mocker.post("https://endoc.ethz.ch/graphql", json=mock_document_search_response)
    
    client = EndocClient(api_key="fake-api-key")
    result = client.document_search(ranking_variable="BERT", keywords=["test"])
    
    assert result.status == "SUCCESS"
    assert result.response.paper_list[0].id_value == "221802394"