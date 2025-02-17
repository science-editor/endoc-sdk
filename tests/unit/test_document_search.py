def test_document_search(dummy_doc_search_service):
    result = dummy_doc_search_service.search_documents("BERT", keywords=["test"])
    assert result.status == "success"
    assert result.response.search_stats.nMatchingDocuments == "14318924"
    assert result.response.paper_list[0].id_value == "221802394"