from .services.document_search import DocumentSearchService
from .services.paginated_search import PaginatedSearchService
from .services.summarization import SummarizationService
from .services.single_paper_search import SinglePaperSearchService
from .services.get_note_library import GetNoteLibraryService

class EndocClient:
    def __init__(self, api_key: str):
        self._summarization_service = SummarizationService(api_key)
        self._document_search_service = DocumentSearchService(api_key)
        self._paginated_search_service = PaginatedSearchService(api_key)
        self._single_paper_service = SinglePaperSearchService(api_key)
        self._get_note_library_service = GetNoteLibraryService(api_key)
        self._custom_services = {}

    def summarize(self, id_value: str):
        return self._summarization_service.summarize_paper(id_value)

    def document_search(self, ranking_variable: str, keywords=None):
        return self._document_search_service.search_documents(ranking_variable, keywords)

    def paginated_search(self, paper_list, keywords=None):
        return self._paginated_search_service.paginated_search(paper_list, keywords)

    def single_paper(self, id_value: str):
        return self._single_paper_service.get_single_paper(id_value)

    def get_note_library(self, doc_id: str):
        return self._get_note_library_service.get_note_library(doc_id)

    def register_service(self, name: str, service_callable):
        """Register a custom service function under the given name."""
        self._custom_services[name] = service_callable

    def __getattr__(self, name: str):
        """If the attribute isn't found, look it up in the custom services."""
        if name in self._custom_services:
            return self._custom_services[name]
        raise AttributeError(f"'EndocClient' object has no attribute '{name}'")