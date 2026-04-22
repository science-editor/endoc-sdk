from endoc.endoc_client import EndocClient
from endoc.models.pdf_import import ImportPDFData
from endoc.services.pdf_import import PDFImportService


VALIDATE_RESPONSE = {
    "data": {
        "documentSearch": {
            "status": "SUCCESS",
            "message": "This user is authorized",
            "response": None,
        }
    }
}

IMPORT_RESPONSE = {
    "data": {
        "importPDFWithAPIKey": {
            "status": "success",
            "message": "PDFs imported",
            "response": [
                {
                    "_id": "bookmark_1",
                    "id_value": "221802394",
                    "id_field": "id_int",
                    "id_type": "int",
                    "id_collection": "S2AG",
                }
            ],
        }
    }
}


def test_pdf_import_service_success(mock_api_client):
    _, mocker = mock_api_client
    mocker.post(
        "https://endoc.ethz.ch/graphql",
        additional_matcher=lambda req: "documentSearch" in req.text,
        json=VALIDATE_RESPONSE,
    )
    mocker.post(
        "https://endoc.ethz.ch/graphql",
        additional_matcher=lambda req: "importPDFWithAPIKey" in req.text,
        json=IMPORT_RESPONSE,
    )

    service = PDFImportService(api_key="fake-api-key")
    result = service.import_pdf_with_api_key(["JVBERi0xLjcK"])

    assert isinstance(result, ImportPDFData)
    assert result.status == "success"
    assert result.response is not None
    assert result.response[0].id_value == "221802394"


def test_pdf_import_service_invalid_input(mock_api_client):
    _, mocker = mock_api_client
    mocker.post(
        "https://endoc.ethz.ch/graphql",
        additional_matcher=lambda req: "documentSearch" in req.text,
        json=VALIDATE_RESPONSE,
    )

    service = PDFImportService(api_key="fake-api-key")

    try:
        service.import_pdf_with_api_key([])
        assert False, "Expected ValueError"
    except ValueError as err:
        assert "base64list must be a non-empty list" in str(err)


def test_import_pdfs_from_folder_batches(tmp_path, mock_api_client):
    _, mocker = mock_api_client
    mocker.post(
        "https://endoc.ethz.ch/graphql",
        additional_matcher=lambda req: "documentSearch" in req.text,
        json=VALIDATE_RESPONSE,
    )
    mocker.post(
        "https://endoc.ethz.ch/graphql",
        additional_matcher=lambda req: "importPDFWithAPIKey" in req.text,
        json=IMPORT_RESPONSE,
    )

    (tmp_path / "a.pdf").write_bytes(b"%PDF-1.4 fake a")
    (tmp_path / "b.pdf").write_bytes(b"%PDF-1.4 fake b")

    client = EndocClient(api_key="fake-api-key")
    responses = client.import_pdfs_from_folder(str(tmp_path), batch_size=1)

    assert len(responses) == 2
    assert all(isinstance(item, ImportPDFData) for item in responses)
