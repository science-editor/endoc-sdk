from pydantic import BaseModel
from typing import List, Optional

class NoteLibraryItem(BaseModel):
    _id: str
    id_value: str
    id_field: str
    id_type: str
    id_collection: str

class GetNoteLibraryResponse(BaseModel):
    status: Optional[str] = None
    message: Optional[str] = None
    response: Optional[List[NoteLibraryItem]] = None