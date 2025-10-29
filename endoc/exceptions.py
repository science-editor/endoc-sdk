class EndocError(Exception):
    """Base error for all Endoc SDK exceptions."""

class AuthenticationError(EndocError):
    """API key is missing, invalid, or expired."""

class PermissionError(EndocError):
    """API key is valid but lacks permission for the resource."""

class RateLimitError(EndocError):
    """You are sending requests too quickly."""

class APIError(EndocError):
    """Non-auth server errors or malformed responses."""
    