from pydantic import BaseModel
from typing import List, Optional

class Author(BaseModel):
    FamilyName: str
    GivenName: str

class PublicationDate(BaseModel):
    Year: Optional[int] = None
    Month: Optional[int] = None
    Day: Optional[int] = None
    Name: Optional[str] = None

class PaperID(BaseModel):
    collection: str
    id_field: str
    id_type: str
    id_value: str

class PaperReference(BaseModel):
    Title: str
    Author: List[Author]
    Venue: str
    PublicationDate: PublicationDate
    ReferenceText: str
    PaperID: Optional["PaperID"] = None

class SinglePaperContent(BaseModel):
    Abstract: str
    Abstract_Parsed: List[dict]
    Fullbody_Parsed: List[dict]
    Fullbody: str

class SinglePaperResponseBody(BaseModel):
    _id: str
    id_int: int
    DOI: str
    Title: str
    Content: SinglePaperContent
    Author: List[Author]
    Venue: str
    PublicationDate: PublicationDate
    Reference: List[PaperReference]

class SinglePaperData(BaseModel):
    status: str
    message: str
    response: SinglePaperResponseBody