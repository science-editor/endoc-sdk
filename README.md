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

Endoc SDK is a Python library for advanced paper search, PDF import, summarization, and note management via a GraphQL API. It uses [Pydantic](https://pydantic-docs.helpmanual.io/) for data validation, returning all responses as typed Python objects.

## Features

- **PDF Import:** Upload local PDFs (single file, multiple files, or entire folders) with auto-fetched full paper data including title, authors, abstract, parsed sections, and references.
- **Document Search:** Search and filter papers using ranking variables and keywords.
- **Single Paper:** Retrieve detailed paper data by ID from any collection.
- **Paginated Search:** Retrieve paginated search results with highlighting.
- **Summarization:** Generate summaries for individual papers.
- **Title Search:** Find papers by title.
- **Note Library:** Retrieve papers associated with a note.
- **Custom Services:** Extend the client with your own composite functions.

## Installation

```bash
pip install endoc
```

## Setup

1. **Obtain your API key** at [endoc.ethz.ch](https://endoc.ethz.ch):
   - Sign up with your Switch Edu-ID credentials.
   - Go to **Account** → **Developer API** → **Generate**.
   - Copy the API key.

2. **Create a `.env` file** in your project root:
   ```
   ENDOC_API_KEY=your_api_key_here
   ```

3. **Load environment variables:**
   ```bash
   pip install python-dotenv
   ```
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

4. **Instantiate the client:**
   ```python
   from endoc import EndocClient

   client = EndocClient(api_key="your_api_key_here")
   # or, if ENDOC_API_KEY is set in .env:
   client = EndocClient(api_key=None)
   ```

5. **(Optional) Override the GraphQL endpoint:**
   ```
   ENDOC_GRAPHQL_URL=http://localhost:9000/graphql
   ```
   The SDK resolves the URL in this order: `ENDOC_GRAPHQL_URL` → `STAGING_GRAPHQL_URL` → `PROD_GRAPHQL_URL` → `https://endoc.ethz.ch/graphql`.

## Usage

### PDF Import

Upload PDFs and get back rich paper objects with full metadata, parsed sections, and references.

```python
from endoc import EndocClient

client = EndocClient(api_key="your_key")

# Single file
result = client.import_pdf(path="paper.pdf")

# Multiple files
result = client.import_pdf(paths=["paper1.pdf", "paper2.pdf"])

# Entire folder
result = client.import_pdf(folder="Papers/", recursive=True)

# Access the result
print(result.status)       # "success"
print(len(result.papers))  # number of uploaded papers

paper = result.papers[0]
print(paper.title)         # "Enhancing Academic Networking..."
print(paper.authors)       # [Author(GivenName="Grigor", FamilyName="Dochev"), ...]
print(paper.sections)      # list of parsed sections
print(paper.references)    # list of extracted references
print(paper.fullbody)      # raw full body text
print(paper.abstract)      # abstract text
print(paper.doi)           # DOI string
print(paper.year)          # publication year
```

**Parameters:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `path` | `str \| Path` | — | Single PDF file path |
| `paths` | `list` | — | List of PDF file paths |
| `folder` | `str \| Path` | — | Directory containing PDFs |
| `base64_list` | `list` | — | Raw base64-encoded PDF strings |
| `recursive` | `bool` | `False` | Scan subfolders (folder mode) |
| `max_file_mb` | `int` | `50` | Skip files larger than this |
| `batch_size` | `int` | `10` | Upload in batches of this size |
| `include_references` | `bool` | `False` | Include matched reference papers |

**Return type:** `ImportResult` with `.status`, `.message`, `.papers` (list of `ImportedPaper`), and `.bookmarks` (raw bookmark IDs).

### Document Search

```python
result = client.document_search(
    ranking_variable="BERT",
    keywords=["AvailableField:Content.Fullbody_Parsed"],
)

print(result.status)
print(result.response.search_stats.nMatchingDocuments)

for paper in result.response.paper_list[:5]:
    print(f"{paper.collection}/{paper.id_value}")
```

### Single Paper

Retrieve full paper data by ID. Works with any collection (`S2AG`, `PMCOA`, `UserUploaded`, etc.).

```python
# From Semantic Scholar
result = client.single_paper("221802394")
print(result.response.Title)

# From a user-uploaded paper
result = client.single_paper(
    id_value="1001",
    collection="UserUploaded",
    id_field="id_int",
    id_type="int",
)
print(result.response.Title)
print(result.response.Content.Fullbody_Parsed)
```

### Paginated Search

```python
result = client.paginated_search(
    paper_list=[{
        "collection": "S2AG",
        "id_field": "id_int",
        "id_type": "int",
        "id_value": "221802394",
    }],
    keywords=["machine learning"],
)

print(result.status)
print(len(result.response))
```

### Summarize Paper

```python
result = client.summarize("221802394")

print(result.status)
for sentence in result.response:
    print(f"[{sentence.tag}] {sentence.sentence_text}")
```

### Title Search

```python
result = client.title_search(titles=["Attention Is All You Need"])

for paper in result.response:
    if paper.found:
        print(f"{paper.Title} → {paper.collection}/{paper.id_value}")
```

### Note Library

Retrieve papers associated with a note. Find your note ID from the URL, e.g. `https://endoc.ethz.ch/note/679a1e2e5b25cf001a7c7157` → `679a1e2e5b25cf001a7c7157`.

```python
result = client.get_note_library("679a1e2e5b25cf001a7c7157")

for paper in result.response:
    print(f"{paper.id_collection}/{paper.id_value}")
```

## Extending the Client

### Using the decorator

```python
from endoc import register_service

@register_service("combined_search")
def combined_search(self, paper_list, id_value):
    paginated = self.paginated_search(paper_list, keywords=["example"])
    single = self.single_paper(id_value)
    return {"paginated": paginated, "single": single}

result = client.combined_search(paper_list, "221802394")
```

### Using the method

```python
def my_search(paper_list, id_value):
    paginated = client.paginated_search(paper_list, keywords=["custom"])
    single = client.single_paper(id_value)
    return {"paginated": paginated, "single": single}

client.register_service("my_search", my_search)
result = client.my_search(paper_list, "221802394")
```

## Package Structure

```
endoc/
├── __init__.py
├── client.py              # Low-level GraphQL API client
├── decorators.py          # @register_service decorator
├── endoc_client.py        # High-level EndocClient with all methods
├── exceptions.py          # SDK exception hierarchy
├── queries.py             # GraphQL queries and mutations
├── utils.py               # Shared utilities
├── models/
│   ├── document_search.py
│   ├── note_library.py
│   ├── paginated_search.py
│   ├── pdf_import.py      # ImportResult, ImportedPaper, ImportedBookmark
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
```

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `ENDOC_API_KEY` | Yes | Your Endoc API key |
| `ENDOC_GRAPHQL_URL` | No | Override the GraphQL endpoint |

## Testing

```bash
pip install pytest
python -m pytest
```

Tests are in `tests/unit/` with fixtures in `tests/fixtures/`. Shared setup lives in `tests/conftest.py`.

## Contributing

Contributions are welcome. Please open issues or submit pull requests on the [GitHub repository](https://github.com/science-editor/endoc-sdk). Include tests for any new functionality.

## License

MIT
