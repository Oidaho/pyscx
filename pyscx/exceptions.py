class PyscxError(Exception):
    """Base exception class for all exceptions raised by the Pyscx library."""


class TokenError(PyscxError):
    """Exception raised for errors related to authentication tokens.

    This can include issues such as invalid token format, expired tokens, or
    missing tokens when required for API access.
    """
