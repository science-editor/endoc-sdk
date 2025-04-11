import pytest
import requests_mock
from gql import Client
from gql.transport.requests import RequestsHTTPTransport
from endoc.client import APIClient

@pytest.fixture
def mock_api_client():
    """Fixture for a mock APIClient that doesn't hit the real server."""
    with requests_mock.Mocker() as m:
        # Mock the schema fetch with a valid introspection response
        introspection_response = {
            "data": {
                "__schema": {
                    "queryType": {"name": "Query"},
                    "mutationType": None,
                    "subscriptionType": None,
                    "types": [
                        # Standard GraphQL scalar types
                        {"kind": "SCALAR", "name": "String", "fields": None, "interfaces": None},
                        {"kind": "SCALAR", "name": "Float", "fields": None, "interfaces": None},
                        {"kind": "SCALAR", "name": "Boolean", "fields": None, "interfaces": None},
                        {"kind": "SCALAR", "name": "Int", "fields": None, "interfaces": None},
                        {"kind": "SCALAR", "name": "ID", "fields": None, "interfaces": None},
                        # Query type
                        {
                            "kind": "OBJECT",
                            "name": "Query",
                            "fields": [
                                {
                                    "name": "documentSearch",
                                    "args": [
                                        {"name": "ranking_variable", "type": {"kind": "SCALAR", "name": "String"}},
                                        {"name": "keywords", "type": {"kind": "LIST", "ofType": {"kind": "SCALAR", "name": "String"}}},
                                        {"name": "paper_list", "type": {"kind": "LIST", "ofType": {"kind": "INPUT_OBJECT", "name": "MetadataInput"}}},
                                        {"name": "ranking_collection", "type": {"kind": "SCALAR", "name": "String"}},
                                        {"name": "ranking_id_field", "type": {"kind": "SCALAR", "name": "String"}},
                                        {"name": "ranking_id_value", "type": {"kind": "SCALAR", "name": "String"}},
                                        {"name": "ranking_id_type", "type": {"kind": "SCALAR", "name": "String"}},
                                    ],
                                    "type": {"kind": "OBJECT", "name": "DocumentSearch"},
                                },
                                {
                                    "name": "paginatedSearch",
                                    "args": [
                                        {"name": "paper_list", "type": {"kind": "LIST", "ofType": {"kind": "INPUT_OBJECT", "name": "MetadataInput"}}},
                                        {"name": "keywords", "type": {"kind": "LIST", "ofType": {"kind": "SCALAR", "name": "String"}}},
                                    ],
                                    "type": {"kind": "OBJECT", "name": "PaginatedSearch"},
                                },
                                {
                                    "name": "singlePaper",
                                    "args": [
                                        {"name": "paper_id", "type": {"kind": "INPUT_OBJECT", "name": "MetadataInput"}},
                                    ],
                                    "type": {"kind": "OBJECT", "name": "SinglePaper"},
                                },
                                # Added: Summarization query
                                {
                                    "name": "summarizePaper",
                                    "args": [
                                        {"name": "paper_id", "type": {"kind": "INPUT_OBJECT", "name": "MetadataInput"}},
                                    ],
                                    "type": {"kind": "OBJECT", "name": "SummarizationResponse"},
                                },
                            ],
                            "interfaces": [],
                        },
                        # DocumentSearch types
                        {
                            "kind": "OBJECT",
                            "name": "DocumentSearch",
                            "fields": [
                                {"name": "status", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "message", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "response", "args": [], "type": {"kind": "OBJECT", "name": "DocumentSearchResponse", "ofType": None}},
                            ],
                            "interfaces": [],
                        },
                        {
                            "kind": "OBJECT",
                            "name": "DocumentSearchResponse",
                            "fields": [
                                {"name": "search_stats", "args": [], "type": {"kind": "OBJECT", "name": "SearchStats"}},
                                {"name": "paper_list", "args": [], "type": {"kind": "LIST", "ofType": {"kind": "OBJECT", "name": "PaperMetadata"}}},
                                {"name": "reranking_scores", "args": [], "type": {"kind": "LIST", "ofType": {"kind": "SCALAR", "name": "Float"}}},
                                {"name": "prefetching_scores", "args": [], "type": {"kind": "LIST", "ofType": {"kind": "SCALAR", "name": "Float"}}},
                            ],
                            "interfaces": [],
                        },
                        {
                            "kind": "OBJECT",
                            "name": "SearchStats",
                            "fields": [
                                {"name": "DurationTotalSearch", "args": [], "type": {"kind": "SCALAR", "name": "Float"}},
                                {"name": "nMatchingDocuments", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                            ],
                            "interfaces": [],
                        },
                        {
                            "kind": "OBJECT",
                            "name": "PaperMetadata",
                            "fields": [
                                {"name": "collection", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "id_field", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "id_type", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "id_value", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                            ],
                            "interfaces": [],
                        },
                        # PaginatedSearch types
                        {
                            "kind": "OBJECT",
                            "name": "PaginatedSearch",
                            "fields": [
                                {"name": "status", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "message", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "response", "args": [], "type": {"kind": "LIST", "ofType": {"kind": "OBJECT", "name": "PaginatedSearchResponseBody"}}},
                            ],
                            "interfaces": [],
                        },
                        {
                            "kind": "OBJECT",
                            "name": "PaginatedSearchResponseBody",
                            "fields": [
                                {"name": "_id", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "DOI", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "Title", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "Content", "args": [], "type": {"kind": "OBJECT", "name": "Content"}},
                                {"name": "Author", "args": [], "type": {"kind": "LIST", "ofType": {"kind": "OBJECT", "name": "Author"}}},
                                {"name": "Venue", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "PublicationDate", "args": [], "type": {"kind": "OBJECT", "name": "PublicationDate"}},
                                {"name": "id_int", "args": [], "type": {"kind": "SCALAR", "name": "Int"}},
                                {"name": "relevant_sentences", "args": [], "type": {"kind": "LIST", "ofType": {"kind": "SCALAR", "name": "String"}}},
                            ],
                            "interfaces": [],
                        },
                        # SinglePaper types
                        {
                            "kind": "OBJECT",
                            "name": "SinglePaper",
                            "fields": [
                                {"name": "status", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "message", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "response", "args": [], "type": {"kind": "OBJECT", "name": "SinglePaperResponseBody", "ofType": None}},
                            ],
                            "interfaces": [],
                        },
                        {
                            "kind": "OBJECT",
                            "name": "SinglePaperResponseBody",
                            "fields": [
                                {"name": "_id", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "id_int", "args": [], "type": {"kind": "SCALAR", "name": "Int"}},
                                {"name": "DOI", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "Title", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "Content", "args": [], "type": {"kind": "OBJECT", "name": "SinglePaperContent"}},
                                {"name": "Author", "args": [], "type": {"kind": "LIST", "ofType": {"kind": "OBJECT", "name": "Author"}}},
                                {"name": "Venue", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "PublicationDate", "args": [], "type": {"kind": "OBJECT", "name": "PublicationDate"}},
                                {"name": "Reference", "args": [], "type": {"kind": "LIST", "ofType": {"kind": "OBJECT", "name": "PaperReference"}}},
                            ],
                            "interfaces": [],
                        },
                        # Shared types
                        {
                            "kind": "OBJECT",
                            "name": "Content",
                            "fields": [
                                {"name": "Abstract", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "Abstract_Parsed", "args": [], "type": {"kind": "LIST", "ofType": {"kind": "OBJECT", "name": "AbstractParsedItem"}}},
                            ],
                            "interfaces": [],
                        },
                        {
                            "kind": "OBJECT",
                            "name": "SinglePaperContent",
                            "fields": [
                                {"name": "Abstract", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "Abstract_Parsed", "args": [], "type": {"kind": "LIST", "ofType": {"kind": "OBJECT", "name": "AbstractParsedItem"}}},
                                {"name": "Fullbody_Parsed", "args": [], "type": {"kind": "LIST", "ofType": {"kind": "OBJECT", "name": "FullbodyParsedItem"}}},
                                {"name": "Fullbody", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                            ],
                            "interfaces": [],
                        },
                        {
                            "kind": "OBJECT",
                            "name": "AbstractParsedItem",
                            "fields": [
                                {"name": "section_id", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "section_title", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "section_text", "args": [], "type": {"kind": "LIST", "ofType": {"kind": "OBJECT", "name": "SectionText"}}},
                            ],
                            "interfaces": [],
                        },
                        {
                            "kind": "OBJECT",
                            "name": "FullbodyParsedItem",
                            "fields": [
                                {"name": "section_id", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "section_title", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "section_text", "args": [], "type": {"kind": "LIST", "ofType": {"kind": "OBJECT", "name": "SectionText"}}},
                            ],
                            "interfaces": [],
                        },
                        {
                            "kind": "OBJECT",
                            "name": "SectionText",
                            "fields": [
                                {"name": "paragraph_id", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "paragraph_text", "args": [], "type": {"kind": "LIST", "ofType": {"kind": "OBJECT", "name": "ParagraphText"}}},
                            ],
                            "interfaces": [],
                        },
                        {
                            "kind": "OBJECT",
                            "name": "ParagraphText",
                            "fields": [
                                {"name": "sentence_id", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "sentence_text", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "sentence_similarity", "args": [], "type": {"kind": "SCALAR", "name": "Float"}},
                                {"name": "cite_spans", "args": [], "type": {"kind": "LIST", "ofType": {"kind": "OBJECT", "name": "CiteSpan"}}},
                            ],
                            "interfaces": [],
                        },
                        {
                            "kind": "OBJECT",
                            "name": "CiteSpan",
                            "fields": [
                                {"name": "start", "args": [], "type": {"kind": "SCALAR", "name": "Int"}},
                                {"name": "end", "args": [], "type": {"kind": "SCALAR", "name": "Int"}},
                                {"name": "text", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "ref_id", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                            ],
                            "interfaces": [],
                        },
                        {
                            "kind": "OBJECT",
                            "name": "Author",
                            "fields": [
                                {"name": "FamilyName", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "GivenName", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                            ],
                            "interfaces": [],
                        },
                        {
                            "kind": "OBJECT",
                            "name": "PublicationDate",
                            "fields": [
                                {"name": "Year", "args": [], "type": {"kind": "SCALAR", "name": "Int"}},
                                {"name": "Month", "args": [], "type": {"kind": "SCALAR", "name": "Int"}},
                                {"name": "Day", "args": [], "type": {"kind": "SCALAR", "name": "Int", "ofType": None}},
                                {"name": "Name", "args": [], "type": {"kind": "SCALAR", "name": "String", "ofType": None}},
                            ],
                            "interfaces": [],
                        },
                        {
                            "kind": "OBJECT",
                            "name": "PaperReference",
                            "fields": [
                                {"name": "Title", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "Author", "args": [], "type": {"kind": "LIST", "ofType": {"kind": "OBJECT", "name": "Author"}}},
                                {"name": "Venue", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "PublicationDate", "args": [], "type": {"kind": "OBJECT", "name": "PublicationDate"}},
                                {"name": "ReferenceText", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "PaperID", "args": [], "type": {"kind": "OBJECT", "name": "PaperID", "ofType": None}},
                            ],
                            "interfaces": [],
                        },
                        {
                            "kind": "OBJECT",
                            "name": "PaperID",
                            "fields": [
                                {"name": "collection", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "id_field", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "id_type", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "id_value", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                            ],
                            "interfaces": [],
                        },
                        # Summarization types (added)
                        {
                            "kind": "OBJECT",
                            "name": "SummarizationResponse",
                            "fields": [
                                {"name": "status", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "message", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "response", "args": [], "type": {"kind": "LIST", "ofType": {"kind": "OBJECT", "name": "SummarizationItem"}}},
                            ],
                            "interfaces": [],
                        },
                        {
                            "kind": "OBJECT",
                            "name": "SummarizationItem",
                            "fields": [
                                {"name": "paragraph_id", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "section_id", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "sentence_id", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "sentence_text", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "tag", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                            ],
                            "interfaces": [],
                        },
                        # MetadataInput type
                        {
                            "kind": "INPUT_OBJECT",
                            "name": "MetadataInput",
                            "inputFields": [
                                {"name": "collection", "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "id_field", "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "id_type", "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "id_value", "type": {"kind": "SCALAR", "name": "String"}},
                            ],
                            "interfaces": None,
                        },
                    ],
                    "directives": [
                        {
                            "name": "include",
                            "locations": ["FIELD", "FRAGMENT_SPREAD", "INLINE_FRAGMENT"],
                            "args": [
                                {"name": "if", "type": {"kind": "NON_NULL", "ofType": {"kind": "SCALAR", "name": "Boolean"}}}
                            ],
                        },
                        {
                            "name": "skip",
                            "locations": ["FIELD", "FRAGMENT_SPREAD", "INLINE_FRAGMENT"],
                            "args": [
                                {"name": "if", "type": {"kind": "NON_NULL", "ofType": {"kind": "SCALAR", "name": "Boolean"}}}
                            ],
                        },
                    ],
                }
            }
        }
        
        # Match introspection request (contains "__schema" in the query)
        m.register_uri(
            "POST",
            "https://endoc.ethz.ch/graphql",
            additional_matcher=lambda req: "__schema" in req.text,
            json=introspection_response
        )
        
        api_client = APIClient(api_key="fake-api-key")
        yield api_client, m