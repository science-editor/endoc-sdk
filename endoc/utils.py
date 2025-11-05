from .exceptions import AuthenticationError, APIError

_OK_STATUSES = {"ok", "success", "successful", "done"}

def is_auth_error_message(message: str) -> bool:
    msg_l = (message or "").lower()
    return any(
        kw in msg_l
        for kw in (
            "unauth",
            "invalid api key",
            "missing api key",
            "expired api key",
            "not authorized",
            "forbidden",
            "token invalid",
            "token expired",
        )
    )

def raise_for_domain_errors(block: dict) -> None:
    """
    Given an operation block like:
      {"status": "...", "message": "...", "response": ...}
    Raise AuthenticationError for auth-related failures, APIError otherwise.
    """
    if not isinstance(block, dict):
        return

    status = (block.get("status") or "").strip().lower()
    message = (block.get("message") or "").strip()

    if status in _OK_STATUSES:
        return

    if is_auth_error_message(message):
        raise AuthenticationError(message or "Invalid or missing API key.")

    if status or message:
        raise APIError(message or f"Operation failed with status='{status}'.")
