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
                        {
                            "kind": "SCALAR",
                            "name": "String",
                            "fields": None,
                            "interfaces": None,
                        },
                        {
                            "kind": "SCALAR",
                            "name": "Float",
                            "fields": None,
                            "interfaces": None,
                        },
                        {
                            "kind": "SCALAR",
                            "name": "Boolean",
                            "fields": None,
                            "interfaces": None,
                        },
                        {
                            "kind": "SCALAR",
                            "name": "Int",
                            "fields": None,
                            "interfaces": None,
                        },
                        {
                            "kind": "SCALAR",
                            "name": "ID",
                            "fields": None,
                            "interfaces": None,
                        },
                        # Custom types for documentSearch
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
                                }
                            ],
                            "interfaces": [],
                        },
                        {
                            "kind": "OBJECT",
                            "name": "DocumentSearch",
                            "fields": [
                                {"name": "status", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "message", "args": [], "type": {"kind": "SCALAR", "name": "String"}},
                                {
                                    "name": "response",
                                    "args": [],
                                    "type": {
                                        "kind": "OBJECT",
                                        "name": "DocumentSearchResponse",
                                        "ofType": None  # Indicates nullable
                                    },
                                },
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
                        # Add MetadataInput type
                        {
                            "kind": "INPUT_OBJECT",
                            "name": "MetadataInput",
                            "inputFields": [
                                {"name": "collection", "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "id_field", "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "id_type", "type": {"kind": "SCALAR", "name": "String"}},
                                {"name": "id_value", "type": {"kind": "SCALAR", "name": "String"}},
                            ],
                            "interfaces": None,  # Input objects don’t have interfaces
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