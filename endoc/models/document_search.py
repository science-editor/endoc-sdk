from pydantic import BaseModel
from typing import List, Optional

class DocumentSearchStats(BaseModel):
    DurationTotalSearch: float
    nMatchingDocuments: str

class PaperMetadata(BaseModel):
    collection: str
    id_field: str
    id_type: str
    id_value: str

class DocumentSearchResponseBody(BaseModel):
    search_stats: DocumentSearchStats
    paper_list: List[PaperMetadata]
    reranking_scores: List[float]
    prefetching_scores: List[float]

class DocumentSearchData(BaseModel):
    status: str
    message: str
    response: Optional[DocumentSearchResponseBody] = None