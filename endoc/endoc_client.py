import base64
from pathlib import Path
from typing import List, Optional, Union

from .services.document_search import DocumentSearchService
from .services.paginated_search import PaginatedSearchService
from .services.summarization import SummarizationService
from .services.single_paper_search import SinglePaperSearchService
from .services.get_note_library import GetNoteLibraryService
from .services.title_search import TitleSearchService
from .services.pdf_import import PDFImportService
from .models.pdf_import import ImportResult, ImportedPaper


class EndocClient:
    def __init__(self, api_key: str):
        self._summarization_service = SummarizationService(api_key)
        self._document_search_service = DocumentSearchService(api_key)
        self._paginated_search_service = PaginatedSearchService(api_key)
        self._single_paper_service = SinglePaperSearchService(api_key)
        self._get_note_library_service = GetNoteLibraryService(api_key)
        self._title_search_service = TitleSearchService(api_key)
        self._pdf_import_service = PDFImportService(api_key)
        self._custom_services = {}

    # ── Existing query methods ──────────────────────────────────────────

    def summarize(self, id_value: str):
        return self._summarization_service.summarize_paper(id_value)

    def document_search(self, ranking_variable: str, keywords=None):
        return self._document_search_service.search_documents(ranking_variable, keywords)

    def paginated_search(self, paper_list, keywords=None):
        return self._paginated_search_service.paginated_search(paper_list, keywords)

    def single_paper(
        self,
        id_value: str,
        collection: str = "S2AG",
        id_field: str = "id_int",
        id_type: str = "int",
    ):
        return self._single_paper_service.get_single_paper(
            id_value, collection=collection, id_field=id_field, id_type=id_type
        )

    def get_note_library(self, doc_id: str):
        return self._get_note_library_service.get_note_library(doc_id)

    def title_search(self, titles):
        return self._title_search_service.title_search(titles)

    # ── PDF Import ──────────────────────────────────────────────────────

    def import_pdf(
        self,
        path: Optional[Union[str, Path]] = None,
        paths: Optional[List[Union[str, Path]]] = None,
        folder: Optional[Union[str, Path]] = None,
        base64_list: Optional[List[str]] = None,
        *,
        recursive: bool = False,
        max_file_mb: int = 50,
        batch_size: int = 10,
        include_references: bool = False,
    ) -> ImportResult:
        """Upload PDFs to Endoc and return full paper data.

        Provide exactly one of the input parameters:
            path         – a single PDF file path
            paths        – a list of PDF file paths
            folder       – a directory containing PDFs
            base64_list  – raw base64-encoded PDF strings

        Args:
            recursive:          Scan subfolders when using ``folder``.
            max_file_mb:        Skip files larger than this (MB).
            batch_size:         Upload in batches of this size.
            include_references: If True, include reference papers matched
                                by the NLP service. If False (default),
                                only return the papers you uploaded
                                (collection == "UserUploaded").

        Returns:
            ImportResult with .papers (list of ImportedPaper) containing
            full paper data (title, authors, abstract, sections, etc.).
        """
        # ── Validate input ──────────────────────────────────────────────
        inputs = sum(x is not None for x in [path, paths, folder, base64_list])
        if inputs == 0:
            raise ValueError(
                "Provide one of: path, paths, folder, or base64_list."
            )
        if inputs > 1:
            raise ValueError(
                "Provide only one of: path, paths, folder, or base64_list."
            )

        # ── Build base64 payloads ───────────────────────────────────────
        if base64_list is not None:
            encoded = base64_list
        elif path is not None:
            encoded = [self._encode_pdf(Path(path))]
        elif paths is not None:
            encoded = [self._encode_pdf(Path(p)) for p in paths]
        else:
            encoded = self._encode_folder(
                Path(folder), recursive=recursive, max_file_mb=max_file_mb
            )

        if not encoded:
            raise ValueError("No valid PDF files to upload.")

        # ── Upload in batches ───────────────────────────────────────────
        all_bookmarks = []
        last_status = "success"
        last_message = ""

        for i in range(0, len(encoded), batch_size):
            batch = encoded[i : i + batch_size]
            result = self._pdf_import_service.import_pdf_with_api_key(batch)
            last_status = result.status
            last_message = result.message
            if result.response:
                all_bookmarks.extend(result.response)

        # ── Filter ──────────────────────────────────────────────────────
        if not include_references:
            filtered = [
                bk for bk in all_bookmarks
                if bk.id_collection == "UserUploaded"
            ]
        else:
            filtered = all_bookmarks

        # ── Auto-fetch full paper data ──────────────────────────────────
        papers = []
        for bk in filtered:
            try:
                paper_data = self.single_paper(
                    id_value=bk.id_value,
                    collection=bk.id_collection,
                    id_field=bk.id_field,
                    id_type=bk.id_type,
                )
            except Exception:
                paper_data = None

            papers.append(
                ImportedPaper.from_bookmark_and_paper(bk, paper_data)
            )

        return ImportResult(
            status=last_status,
            message=last_message,
            papers=papers,
            bookmarks=all_bookmarks,
        )

    # ── Private helpers ─────────────────────────────────────────────────

    @staticmethod
    def _encode_pdf(pdf_path: Path) -> str:
        pdf_path = pdf_path.expanduser().resolve()
        if not pdf_path.exists() or not pdf_path.is_file():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")
        if pdf_path.suffix.lower() != ".pdf":
            raise ValueError(f"Not a PDF file: {pdf_path}")
        with pdf_path.open("rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    @staticmethod
    def _encode_folder(
        folder: Path,
        recursive: bool = False,
        max_file_mb: int = 50,
    ) -> List[str]:
        folder = folder.expanduser().resolve()
        if not folder.exists() or not folder.is_dir():
            raise ValueError(f"Folder not found: {folder}")

        pattern = "**/*.pdf" if recursive else "*.pdf"
        pdf_paths = sorted(p for p in folder.glob(pattern) if p.is_file())
        if not pdf_paths:
            raise ValueError(f"No PDF files found in: {folder}")

        encoded = []
        for p in pdf_paths:
            if p.stat().st_size / (1024 * 1024) > max_file_mb:
                continue
            with p.open("rb") as f:
                encoded.append(base64.b64encode(f.read()).decode("utf-8"))
        return encoded

    # ── Custom services ─────────────────────────────────────────────────

    def register_service(self, name: str, service_callable):
        """Register a custom service function under the given name."""
        self._custom_services[name] = service_callable

    def __getattr__(self, name: str):
        if name in self._custom_services:
            return self._custom_services[name]
        raise AttributeError(f"'EndocClient' object has no attribute '{name}'")
