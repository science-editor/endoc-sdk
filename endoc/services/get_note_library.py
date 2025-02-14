from ..client import APIClient
from ..queries import GET_NOTE_LIBRARY_QUERY
from ..models.note_library import GetNoteLibraryResponse

class GetNoteLibraryService:
    def __init__(self, api_key: str):
        self.client = APIClient(api_key)

    def get_note_library(self, doc_id: str):
        variable_values = {"doc_id": doc_id}
        raw_result = self.client.execute_query(GET_NOTE_LIBRARY_QUERY, variable_values)
        data = raw_result.get("getNoteLibrary")
        if not data:
            raise ValueError("No 'getNoteLibrary' key found in response.")
        return GetNoteLibraryResponse(**data)