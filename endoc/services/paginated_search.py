from ..client import APIClient
from ..queries import PAGINATED_SEARCH_QUERY
from ..models.paginated_search import PaginatedSearchData

class PaginatedSearchService:
    def __init__(self, api_key):
        self.client = APIClient(api_key)

    def paginated_search(self, paper_list, keywords=None):
        variable_values = {
            "paper_list": paper_list,
            "keywords": keywords or [],
        }
        raw_result = self.client.execute_query(PAGINATED_SEARCH_QUERY, variable_values)
        data = raw_result.get("paginatedSearch")
        if not data:
            raise ValueError("No 'paginatedSearch' key found in response.")
        return PaginatedSearchData(**data)