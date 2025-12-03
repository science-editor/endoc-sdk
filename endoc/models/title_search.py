from pydantic import BaseModel
from typing import List, Optional, Union

class TitleSearchAuthor(BaseModel):
    FamilyName: str
    GivenName: str

class TitleSearchItem(BaseModel):
    Title: str
    found: bool

    collection: Optional[str] = None
    id_field: Optional[str] = None
    id_type: Optional[str] = None
    id_value: Optional[Union[str, int]] = None

    Author: Optional[List[TitleSearchAuthor]] = None

class TitleSearchData(BaseModel):
    status: str
    message: str
    response: Optional[List[TitleSearchItem]] = None