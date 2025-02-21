from pydantic import BaseModel, field_validator
from typing import List, Optional

class Author(BaseModel):
    FamilyName: str
    GivenName: str

class PublicationDate(BaseModel):
    Year: Optional[int] = None
    Month: Optional[int] = None
    Day: Optional[int] = None
    Name: Optional[str] = None

    @field_validator("Year", "Month", "Day", mode="before")
    def empty_str_to_none(cls, value):
        if isinstance(value, str) and value.strip() == "":
            return None
        return value
    
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