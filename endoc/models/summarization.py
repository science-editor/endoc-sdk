from pydantic import BaseModel
from typing import List

class SummarizationItem(BaseModel):
    paragraph_id: str
    section_id: str
    sentence_id: str
    sentence_text: str
    tag: str

class SummarizationResponseData(BaseModel):
    status: str
    message: str
    response: List[SummarizationItem]