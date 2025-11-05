from __future__ import annotations

import os
from typing import Any, Dict, Optional

from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from .utils import raise_for_domain_errors, is_auth_error_message

try:
    from gql.transport.exceptions import TransportQueryError, TransportServerError
except ImportError:
    try:
        from gql.transport import exceptions as _gql_ex
        TransportQueryError = getattr(_gql_ex, "TransportQueryError", Exception)
        TransportServerError = getattr(_gql_ex, "TransportServerError", Exception)
    except Exception:
        class TransportQueryError(Exception):
            def __init__(self, message: str | None = None, errors=None):
                super().__init__(message or "Transport query error")
                self.errors = errors or []

        class TransportServerError(Exception):
            def __init__(self, message: str | None = None, status_code: int | None = None):
                super().__init__(message or "Transport server error")
                self.status_code = status_code

from .exceptions import (
    AuthenticationError,
    PermissionError,
    RateLimitError,
    APIError,
)
from .utils import raise_for_domain_errors

GRAPHQL_URL = "https://endoc.ethz.ch/graphql"
DEFAULT_TIMEOUT = 30  # seconds

VALIDATE_QUERY = gql("""
query Validate {
  documentSearch {
    status
    message
    response { __typename }  # tiny payload; unused
  }
}
""")

def _map_http_transport_error(err: TransportServerError) -> None:
    """Map HTTP status codes to SDK exceptions."""
    status = getattr(err, "status_code", None)
    if status == 401:
        raise AuthenticationError("Invalid or missing API key (HTTP 401).") from err
    if status == 403:
        raise PermissionError("API key lacks permission (HTTP 403).") from err
    if status == 429:
        raise RateLimitError("Rate limit exceeded (HTTP 429).") from err
    if status and 500 <= status < 600:
        raise APIError(f"Server error (HTTP {status}).") from err
    raise APIError(str(err)) from err

def _map_graphql_error(err: TransportQueryError) -> None:
    """
    GraphQL errors (HTTP 200 with errors array). Translate via extensions.code.
    """
    errors = getattr(err, "errors", None) or []
    first = errors[0] if errors else {}
    extensions = first.get("extensions") or {}
    code = (extensions.get("code") or "").upper()
    message = first.get("message") or str(err)

    if code == "UNAUTHENTICATED":
        raise AuthenticationError(message) from err
    if code in {"FORBIDDEN", "INSUFFICIENT_PERMISSIONS"}:
        raise PermissionError(message) from err
    if code == "RATE_LIMITED":
        raise RateLimitError(message) from err
    raise APIError(message) from err

class APIClient:
    """Low-level GraphQL client with automatic API key validation and consistent errors."""

    def __init__(
        self,
        api_key: Optional[str],
        *,
        timeout: int = DEFAULT_TIMEOUT,
        user_agent: Optional[str] = None,
    ):
        key = api_key or os.getenv("ENDOC_API_KEY") or os.getenv("API_KEY")
        if not key:
            raise AuthenticationError("No API key provided. Set ENDOC_API_KEY or pass api_key=...")

        headers = {"x-api-key": key}
        if user_agent:
            headers["User-Agent"] = user_agent

        self.transport = RequestsHTTPTransport(
            url=GRAPHQL_URL,
            headers=headers,
            use_json=True,
            timeout=timeout,
        )

        self.client = Client(
            transport=self.transport,
            fetch_schema_from_transport=False,
        )

        self._validate_api_key()

    from .utils import raise_for_domain_errors, is_auth_error_message

    def _validate_api_key(self) -> None:
        try:
            data = self.client.execute(VALIDATE_QUERY)
            block = data.get("documentSearch") if isinstance(data, dict) else None

            if isinstance(block, dict):
                status = (block.get("status") or "").strip().lower()
                message = (block.get("message") or "").strip()

                if is_auth_error_message(message):
                    raise_for_domain_errors(block)

                return

            return

        except TransportServerError as e:
            _map_http_transport_error(e)
        except TransportQueryError as e:
            _map_graphql_error(e)
        except Exception as e:
            raise APIError(str(e)) from e

    def execute_query(self, query, variable_values: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        try:
            result = self.client.execute(query, variable_values or {})
            if isinstance(result, dict):
                for _, block in result.items():
                    if isinstance(block, dict) and ("status" in block or "message" in block):
                        raise_for_domain_errors(block)
            return result
        except TransportServerError as e:
            _map_http_transport_error(e)
        except TransportQueryError as e:
            _map_graphql_error(e)
        except Exception as e:
            raise APIError(str(e)) from e


def register_service(name):
    def decorator(func):
        from .endoc_client import EndocClient
        setattr(EndocClient, name, func)
        return func
    return decorator
