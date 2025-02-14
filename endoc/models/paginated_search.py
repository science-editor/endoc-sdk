from pydantic import BaseModel
from typing import List, Optional

class AbstractParsedItem(BaseModel):
    section_id: str
    section_title: str
    section_text: List[dict]

class Content(BaseModel):
    Abstract: str
    Abstract_Parsed: List[AbstractParsedItem]

class Author(BaseModel):
    FamilyName: str
    GivenName: str

class PublicationDate(BaseModel):
    Year: int
    Month: int
    Day: Optional[int] = None
    Name: Optional[str] = None

class PaginatedSearchResponseBody(BaseModel):
    _id: str
    DOI: str
    Title: str
    Content: Content
    Author: List[Author]
    Venue: str
    PublicationDate: PublicationDate
    id_int: int
    relevant_sentences: List[str]

class PaginatedSearchData(BaseModel):
    status: str
    message: str
    response: List[PaginatedSearchResponseBody]