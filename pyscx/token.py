from enum import Enum


class TokenType(Enum):
    """Enum representing types of tokens for authentication."""

    USER = "user"
    APPLICATION = "application"


class Token:
    """Authentication token for accessing STALCRAFT: X API endpoints."""

    __slots__ = ("value", "type")

    def __init__(self, value: str, type: TokenType) -> None:
        """Class initialization

        Args:
            value (str): Token value (token itself).
            type (TokenType): Type of the token.
        """
        self.value = value
        self.type = type
