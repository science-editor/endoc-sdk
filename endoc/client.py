from gql import Client
from gql.transport.requests import RequestsHTTPTransport
import os

class APIClient:
    def __init__(self, api_key):
        self.client = Client(
            transport = RequestsHTTPTransport(
                url="https://endoc.ethz.ch/graphql",
                headers={'x-api-key': api_key}
            ),
            fetch_schema_from_transport=True,
        )

    def execute_query(self, query, variable_values=None):
        return self.client.execute(query, variable_values or {})