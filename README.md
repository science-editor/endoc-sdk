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

2. **Create a `.env` File:**
   - In your project's root directory, create a file named `.env`.
   - Add your API key to the file using the following format:
     ```
     API_KEY=your_api_key_here
     ```

3. **Load Environment Variables:**
   - Install [python-dotenv](https://pypi.org/project/python-dotenv/) if you haven't already:
     ```bash
     pip install python-dotenv
     ```
   - In your Python script, load the environment variables at the very start:
     ```python
     from dotenv import load_dotenv
     load_dotenv()
     ```

4. **Instantiate the Endoc client**
    - In your Python script, instantiate a new instance of the `EndocClient`:
    ```python
     client = EndocClient(api_key)
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
├── endoc_client.py
├── decorators.py
├── queries/
│   ├── document_search_query.py
│   ├── get_note_library_query.py
│   ├── paginated_search_query.py
│   ├── single_paper_query.py
│   └── summarize_paper_query.py
├── models/
│   ├── document_search.py
│   ├── note_library.py
│   ├── paginated_search.py
│   ├── single_paper.py
│   └── summarization.py
└── services/
    ├── document_search.py
    ├── get_note_library.py
    ├── paginated_search.py
    ├── single_paper_search.py
    └── summarization.py
```

## Environment Variables

The SDK expects your API key as the environment variable API_KEY. Use a .env file and python-dotenv to load the variable:

```python
from dotenv import load_dotenv
load_dotenv()
```

## Contributing

Contributions are welcome! Please open issues or submit pull requests on the GitHub repository. Ensure that any contributions adhere to the existing code style and include tests where applicable.

## License

This project is licensed under the MIT license.
