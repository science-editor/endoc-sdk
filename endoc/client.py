from gql import Client
from gql.transport.requests import RequestsHTTPTransport
import os

class APIClient:
    def __init__(self, api_key):
        url = os.getenv("STAGING_GRAPHQL_URL")
        self.client = Client(
            transport = RequestsHTTPTransport(
                url=url,
                headers={'x-api-key': api_key}
            ),
            fetch_schema_from_transport=True,
        )

    def execute_query(self, query, variable_values=None):
        return self.client.execute(query, variable_values or {})