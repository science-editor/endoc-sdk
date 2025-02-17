# tests/fixtures/document_search_fixtures.py
import pytest
from endoc.services.document_search import DocumentSearchService
from tests.fixtures.dummy_api import DummyAPIClient

@pytest.fixture
def dummy_doc_search_service(monkeypatch):
    # Override the APIClient in DocumentSearchService with DummyAPIClient
    monkeypatch.setattr("endoc.services.document_search.APIClient", DummyAPIClient)
    return DocumentSearchService(api_key="dummy")
