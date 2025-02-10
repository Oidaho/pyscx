from enum import Enum


class TokenType(Enum):
    """Access token type enum."""

    USER = "user"
    APPLICATION = "application"


class Token(object):
    """The general class of the API access token.
    The interface for transferring a token to an API object.

    Initial Args:
        value (str): Access token.
        type (TokenType): Access token type.
    """

    def __init__(self, value: str, type: TokenType) -> None:
        self.value = value
        self.type = type
