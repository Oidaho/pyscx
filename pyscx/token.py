from enum import Enum


class TokenType(Enum):
    """A list of supported token types for authentication."""

    USER = "user"
    APPLICATION = "application"


class Token(object):
    """API access token class.

    This class provides an interface for passing a token to the API object. Each token consists of
    a value (the actual token string) and its type (which specifies the token's purpose).
    """

    __slots__ = ("value", "type")

    def __init__(self, value: str, type: TokenType) -> None:
        """Initializes a token object with the specified value and type.

        Args:
            value (str): The value of the token.
            type (TokenType): The type of the token, defined in the TokenType Enum.
        """
        self.value = value
        self.type = type
