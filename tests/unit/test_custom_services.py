from endoc import EndocClient, register_service

def test_register_service_decorator():
    client = EndocClient(api_key="fake-api-key")
    
    @register_service("custom_test")
    def custom_test(self):
        return "Hello, World!"
    
    assert hasattr(client, "custom_test")
    assert client.custom_test() == "Hello, World!"

def test_register_service_method():
    client = EndocClient(api_key="fake-api-key")
    
    def custom_service():
        return "Custom Result"
    
    client.register_service("custom_service", custom_service)
    assert client.custom_service() == "Custom Result"

def test_custom_service_combined(mock_api_client, mock_document_search_response):
    _, mocker = mock_api_client
    mocker.post("https://endoc.ethz.ch/graphql", json=mock_document_search_response)
    
    client = EndocClient(api_key="fake-api-key")
    
    @register_service("combined_search")
    def combined_search(self, paper_list, id_value):
        return {
            "paginated": {"status": "SUCCESS", "mocked": True},
            "single": {"status": "SUCCESS", "mocked": True}
        }
    
    paper_list = [{"collection": "S2AG", "id_field": "id_int", "id_type": "int", "id_value": "221802394"}]
    result = client.combined_search(paper_list, "221802394")
    assert "paginated" in result
    assert "single" in result
    assert result["paginated"]["status"] == "SUCCESS"
    assert result["single"]["status"] == "SUCCESS"