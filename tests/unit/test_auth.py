import pytest
from gql.transport.exceptions import TransportServerError, TransportQueryError

from endoc.client import APIClient
from endoc.exceptions import AuthenticationError

class DummyTransportServer401(TransportServerError):
    def __init__(self):
        super().__init__("Unauthorized")
        self.status_code = 401

def test_http_401_maps_to_authentication_error(monkeypatch):
    client = APIClient("bad-key", validate_key=False)

    def boom(*args, **kwargs):
        raise DummyTransportServer401()

    monkeypatch.setattr(client, "execute_query", boom)  # simulate underlying call
    with pytest.raises(AuthenticationError):
        client.execute_query("query { ping }")

def test_graphql_unauthenticated_maps_to_authentication_error(monkeypatch):
    client = APIClient("bad-key", validate_key=False)

    class DummyTQE(TransportQueryError):
        @property
        def errors(self):
            return [{
                "message": "Unauthenticated",
                "extensions": {"code": "UNAUTHENTICATED"},
            }]

    def boom(*args, **kwargs):
        raise DummyTQE("GraphQL error")

    monkeypatch.setattr(client, "execute_query", boom)
    with pytest.raises(AuthenticationError):
        client.execute_query("query { me { id } }")
