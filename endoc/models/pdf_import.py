from pydantic import BaseModel, Field
from typing import List, Optional

from .single_paper import (
    Author,
    PublicationDate,
    PaperReference,
    SinglePaperContent,
)


class ImportedBookmark(BaseModel):
    """Raw bookmark returned by the importPDFWithAPIKey mutation."""

    model_config = {"populate_by_name": True}

    mongo_id: Optional[str] = Field(None, alias="_id")
    id_value: str
    id_field: str
    id_type: str
    id_collection: str


class ImportedPaper(BaseModel):
    """Rich paper object combining bookmark metadata with full paper data."""

    # Bookmark identifiers
    id_value: str
    id_field: str
    id_type: str
    collection: str

    # Full paper data (populated by auto-fetch)
    title: str = ""
    authors: List[Author] = []
    venue: str = ""
    year: Optional[int] = None
    doi: str = ""
    abstract: str = ""
    fullbody: str = ""
    sections: List[dict] = []
    references: List[PaperReference] = []

    @classmethod
    def from_bookmark_and_paper(cls, bookmark: ImportedBookmark, paper_data=None):
        """Build an ImportedPaper from a bookmark and optional full paper data."""
        base = {
            "id_value": bookmark.id_value,
            "id_field": bookmark.id_field,
            "id_type": bookmark.id_type,
            "collection": bookmark.id_collection,
        }

        if paper_data and paper_data.response:
            r = paper_data.response
            content = r.Content
            base.update(
                title=r.Title or "",
                authors=r.Author or [],
                venue=r.Venue or "",
                year=r.PublicationDate.Year if r.PublicationDate else None,
                doi=r.DOI or "",
                abstract=(content.Abstract or "") if content else "",
                fullbody=(content.Fullbody or "") if content else "",
                sections=(content.Fullbody_Parsed or []) if content else [],
                references=r.Reference or [],
            )

        return cls(**base)


class ImportResult(BaseModel):
    """Result of an import_pdf() call with full paper data."""

    status: str
    message: str
    papers: List[ImportedPaper] = []
    bookmarks: List[ImportedBookmark] = []


# Keep for backward compatibility with PDFImportService internals
class ImportPDFData(BaseModel):
    status: str
    message: str
    response: Optional[List[ImportedBookmark]] = None
