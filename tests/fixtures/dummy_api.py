import pytest
import requests_mock
from gql import Client
from gql.transport.requests import RequestsHTTPTransport
from endoc.client import APIClient

@pytest.fixture
def mock_api_client():
    """Fixture for a mock APIClient that doesn't hit the real server."""
    with requests_mock.Mocker() as m:
        # Mock the schema fetch with a minimal valid introspection response
        m.post(
            "https://endoc.ethz.ch/graphql",
            [
                {
                    "json": {
                        "data": {
                            "__schema": {
                                "queryType": {"name": "Query"},
                                "mutationType": None,
                                "subscriptionType": None,
                                "types": [],
                                "directives": []
                            }
                        }
                    }
                },
                # Allow subsequent responses to be set by tests
            ]
        )
        api_client = APIClient(api_key="fake-api-key")
        yield api_client, m