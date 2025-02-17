import pytest
from endoc.endoc_client import EndocClient

@pytest.fixture
def client():
    # Create a dummy EndocClient instance.
    client = EndocClient(api_key="dummy")
    # Register a dummy custom service for testing.
    client.register_service("dummy_service", lambda param: param * 2)
    return client

def test_custom_service_registration(client):
    # Test that the custom service is accessible and works as expected.
    result = client.dummy_service(3)
    assert result == 6

def test_non_existent_service(client):
    with pytest.raises(AttributeError):
        _ = client.non_existent_service
