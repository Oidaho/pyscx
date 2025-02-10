from enum import Enum


class TokenType(Enum):
    """A list of supported token types."""

    USER = "user"
    APPLICATION = "application"


class Token(object):
    """The base class for API access tokens.

    Provides an interface for passing a token to an API object.

    Initial Args:
        value (str): The access token.
        type (TokenType): The type of the access token.
    """

    def __init__(self, value: str, type: TokenType) -> None:
        self.value = value
        self.type = type
