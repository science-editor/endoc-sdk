<div style="text-align: center;">
  <img src="https://drive.google.com/uc?export=view&id=18VZK4uejxuPABSQOAiXK2l2EziYwDvdb" alt="Endoc SDK Logo" style="width:50%;">
</div>

<p align="center">
    <img src="https://img.shields.io/pypi/pyversions/endoc?logo=python&logoColor=%23ffd343&color=%23ffd343" />
    <img src="https://img.shields.io/pypi/l/endoc" />
    <img src="https://img.shields.io/pypi/v/endoc?logo=pypi&logoColor=%23ffd343&color=%23ffd343" />
    <img src="https://img.shields.io/pypi/dm/endoc?style=flat&color=red" />
    <img src="https://img.shields.io/pypi/dd/endoc" />
    <a href="https://endoc.ethz.ch">
        <img src="https://img.shields.io/badge/powered_by-Endoc-blue" alt="Powered by Endoc">
    </a>
</p>

# Endoc SDK

Endoc SDK is a Python library that provides powerful tools for advanced paper search, summarization, and note management using a GraphQL API. It leverages [Pydantic](https://pydantic-docs.helpmanual.io/) for robust data validation and modeling, so that all responses are returned as easy‐to‐use Python objects. In addition, Endoc SDK offers an extensibility mechanism to allow you to create custom composite services without modifying the core code.

## Features

- **Document Search:** Search and filter papers using ranking variables and keywords.
- **Summarize Paper:** Generate summaries for individual papers.
- **Paginated Search:** Retrieve paginated search results.
- **Single Paper Search:** Get detailed information about a single paper.
- **Note Library:** Retrieve papers associated with a note.
- **Title Search:** Resolve papers from title lists.
- **PDF Import (API key flow):** Upload local PDFs for indexing/import.
- **Custom Services:** Easily extend the client with your own functions.

## Installation

Install Endoc SDK via pip:

```bash
pip install endoc
```

## Setup

1. **Obtain Your API Key:**
   - Visit [https://endoc.ethz.ch](https://endoc.ethz.ch) and sign up using your Switch Edu-ID credentials.
   - After logging in, click on the **Account** option in the side panel.
   - Under the **Developer API** section, click **Generate** to create a new API key.
   - Copy the generated API key for later use.

2. **Create a `.env` File (optional):**
   - In your project's root directory, create a file named `.env`.
   - Add your API key to the file using one of these supported keys:
     ```
     ENDOC_API_KEY=your_api_key_here
     # or
     API_KEY=your_api_key_here
     ```

3. **Load Environment Variables (if using `.env`):**
   - Install [python-dotenv](https://pypi.org/project/python-dotenv/) if you haven't already:
     ```bash
     pip install python-dotenv
     ```
   - In your Python script:
     ```python
     from dotenv import load_dotenv
     load_dotenv()
     ```

4. **Instantiate the Endoc client**
    - In your Python script, instantiate `EndocClient`:
    ```python
    client = EndocClient(api_key=None)  # reads ENDOC_API_KEY/API_KEY from env
    # or
    client = EndocClient(api_key="your_api_key_here")
    ```

5. **(Optional) Override GraphQL endpoint**
   - By default the SDK uses:
     `https://endoc.ethz.ch/graphql`
   - To target another deployment (e.g. local gateway), set:
     ```
     ENDOC_GRAPHQL_URL=http://localhost:9000/graphql
     ```

## Basic Usage

### 1) Document Search

To search for papers, call the `document_search` method. This returns a `DocumentSearchData` object.

```python
doc_search_result = client.document_search(
    ranking_variable="BERT",
    keywords=["AvailableField:Content.Fullbody_Parsed"]
)

# Accessing properties:
print(doc_search_result.status)
print(doc_search_result.response.search_stats.nMatchingDocuments)
print(doc_search_result.response.paper_list[0].id_value)
```

### 2) Summarize Paper

Call the summarize method with a paper ID to get a summary. The result is a `SummarizationResponseData` object.

```python
summarize_result = client.summarize("221802394")
# Example usage:
print(summarize_result.status)
# You can further inspect summarize_result.response for detailed summary items.
```

### 3) Paginated Search

Use the `paginated_search` method to retrieve paginated results. Prepare a list of paper metadata as input.

```python
example_paper = {
    "collection": "S2AG",
    "id_field": "id_int",
    "id_type": "int",
    "id_value": "221802394"
}
paper_list = [example_paper]
paginated_result = client.paginated_search(paper_list=paper_list)
# Example usage:
print(paginated_result.status)
```

### 4) Single Paper Search

To fetch detailed information for a single paper, use the `single_paper` method. This returns a `SinglePaperData` object.

```python
single_paper_result = client.single_paper("221802394")
# Example usage:
print(single_paper_result.response.Title)
```

### 5) Get Note Library

Retrieve papers related to a note by calling the `get_note_library` method. This returns a `GetNoteLibraryResponse` object. To find your note ID, navigate to a note on Endoc and copy the last part of the url, e.g. for `https://endoc.ethz.ch/note/679a1e2e5b25cf001a7c7157`, the note's ID is `679a1e2e5b25cf001a7c7157`.

```python
note_library_result = client.get_note_library("679a1e2e5b25cf001a7c7157")
if note_library_result.response:
    print(note_library_result.response[0].id_value)
```

### 6) Import PDFs from local folder

```python
result_batches = client.import_pdfs_from_folder(
    folder_path="/absolute/path/to/pdfs",
    recursive=False,
    max_file_mb=50,
    batch_size=5,
)

for batch in result_batches:
    print(batch.status, batch.message, len(batch.response or []))
```

Or use the example script:

```bash
python examples/upload_pdf.py --folder "/absolute/path/to/pdfs"
```

## Extending the Client with Custom Services

Endoc SDK allows you to add your own composite services without modifying the core code. You have two options:

### Option 1: Using the `register_service` Decorator

Endoc SDK re-exports the register_service decorator, so you can define custom methods that become part of the client interface. For example:

```python
from endoc import register_service

@register_service("combined_search")
def combined_search(self, paper_list, id_value):
    paginated = self.paginated_search(paper_list, keywords=["example"])
    single = self.single_paper(id_value)
    return {"paginated": paginated, "single": single}

result = client.combined_search(paper_list, "221802394")
print("Combined Search Result:", result)
```

### Option 2: Using the `register_service` Method

Alternatively, you can register a custom service function directly on the client instance:

```python
def my_custom_service(paper_list, id_value):
    paginated = client.paginated_search(paper_list, keywords=["custom"])
    single = client.single_paper(id_value)
    return {"paginated": paginated, "single": single}

client.register_service("my_custom_service", my_custom_service)

result = client.my_custom_service(paper_list, "221802394")
print("My Custom Service Result:", result)
```

## Package Structure

The package is organized as follows:

```plaintext
endoc/
├── __init__.py
├── client.py
├── decorators.py
├── endoc_client.py
├── exceptions.py
├── queries.py
├── models/
│   ├── document_search.py
│   ├── note_library.py
│   ├── paginated_search.py
│   ├── pdf_import.py
│   ├── single_paper.py
│   ├── summarization.py
│   └── title_search.py
└── services/
    ├── document_search.py
    ├── get_note_library.py
    ├── paginated_search.py
    ├── pdf_import.py
    ├── single_paper_search.py
    ├── summarization.py
    └── title_search.py
examples/
├── test_document_search.py
└── upload_pdf.py
tests/
├── conftest.py
├── fixtures/
└── unit/
    ├── test_auth.py
    ├── test_custom_services.py
    ├── test_document_search.py
    ├── test_paginated_search.py
    ├── test_pdf_import.py
    ├── test_single_paper.py
    └── test_summarization.py
```

## Environment Variables

Supported variables:

- `ENDOC_API_KEY` or `API_KEY`: API key used by the SDK.
- `ENDOC_GRAPHQL_URL` (optional): override default endpoint (`https://endoc.ethz.ch/graphql`).

Use a `.env` file and `python-dotenv` to load variables:

```python
from dotenv import load_dotenv
load_dotenv()
```

## Testing

Endoc SDK includes a test suite to ensure quality and maintain high coverage. The tests are organized by functionality, making it easy to add new tests or modify existing ones.

- Make sure you have installed `pytest` and any other test dependencies:

	```bash
	pip install pytest
	```

### Running the Tests

In the SDK root (`endoc-sdk/`), run:

```bash
python -m pytest
```

### Test Organization

#### Fixtures

The `tests/fixtures` folder holds reusable components like mock responses and dummy clients (e.g., `dummy_api.py`).

A document_search_fixtures.py file might contain fixtures that set up data or patch classes for document search tests.

#### Unit Tests

Located in `tests/unit`, these tests focus on individual modules or classes, mocking external calls.

For example, `test_document_search.py` might ensure the `DocumentSearchService` parses JSON correctly.

#### Integration Tests

Placed in `tests/integration`, these tests cover how multiple parts of the SDK interact. They may call real endpoints in a staging environment or use more extensive mocks that simulate multi-step workflows.

#### `conftest.py`

Pytest automatically discovers and uses any fixtures defined in `conftest.py`.
You can place shared fixtures here (like a global mock of your API client or environment setup).

## Contributing

Contributions are welcome! Please open issues or submit pull requests on the GitHub repository. Ensure that any contributions adhere to the existing code style and include tests where applicable.

## License

This project is licensed under the MIT license.
