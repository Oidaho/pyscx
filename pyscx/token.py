from enum import Enum


class TokenType(Enum):
    """A list of supported token types for authentication.

    Attributes:
        USER (str): The type for user tokens.
        APPLICATION (str): The type for application tokens.
    """

    USER = "user"
    APPLICATION = "application"


class Token(object):
    """The base class for API access tokens.

    This class provides an interface for passing a token to the API object. Each token consists of
    a value (the actual token string) and its type (which specifies the token's purpose).

    Attributes:
        value (str): The access token string.
        type (TokenType): The type of the access token.

    Initial Args:
        value (str): The access token string.
        type (TokenType): The type of the access token.
    """

    __slots__ = ("value", "type")

    def __init__(self, value: str, type: TokenType) -> None:
        self.value = value
        self.type = type
