from ..client import APIClient
from ..queries import DOCUMENT_SEARCH_QUERY
from ..models.document_search import DocumentSearchData

class DocumentSearchService:
    def __init__(self, api_key: str):
        self.client = APIClient(api_key)

    def search_documents(self, ranking_variable, keywords=None):
        variable_values = {
            "ranking_variable": ranking_variable,
            "keywords": keywords or []
        }
        raw_result = self.client.execute_query(DOCUMENT_SEARCH_QUERY, variable_values)
        doc_search_data = raw_result.get("documentSearch")
        if not doc_search_data:
            raise ValueError("No 'documentSearch' key found in response.")
        return DocumentSearchData(**doc_search_data)