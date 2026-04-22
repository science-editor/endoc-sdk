from ..client import APIClient
from ..queries import IMPORT_PDF_WITH_API_KEY_MUTATION
from ..models.pdf_import import ImportPDFData


class PDFImportService:
    def __init__(self, api_key: str):
        self.client = APIClient(api_key)

    def import_pdf_with_api_key(self, base64list):
        if not isinstance(base64list, list) or not base64list:
            raise ValueError("base64list must be a non-empty list of base64 strings.")

        variables = {"base64list": base64list}
        raw_result = self.client.execute_query(IMPORT_PDF_WITH_API_KEY_MUTATION, variables)
        data = raw_result.get("importPDFWithAPIKey")
        if not data:
            raise ValueError("No 'importPDFWithAPIKey' key found in response.")
        return ImportPDFData(**data)
