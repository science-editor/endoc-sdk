from ..client import APIClient
from ..queries import TITLE_SEARCH_QUERY
from ..models.title_search import TitleSearchData
from typing import Iterable, Union

class TitleSearchService:
    def __init__(self, api_key: str):
        self.client = APIClient(api_key)

    def title_search(self, titles: Union[str, Iterable[str]]):
        if isinstance(titles, str):
            titles = [titles]
        titles = [t for t in titles if isinstance(t, str) and t.strip()]
        if not titles:
            raise ValueError("titles must be a non-empty string or list of strings.")
        variables = {"titles": titles}
        raw = self.client.execute_query(TITLE_SEARCH_QUERY, variables)
        data = raw.get("titleSearch")
        if not data:
            raise ValueError("No 'titleSearch' key found in response.")
        return TitleSearchData(**data)