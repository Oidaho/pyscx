from typing import Any, Collection

from .http import APISession, Server
from .methods import MethodsGroupFabric
from .token import Token, TokenType
from .exceptions import MissingTokenError


class API:
    """API Object Class for interacting with the STALCRAFT: X API.

    This class provides an interface to communicate with the STALCRAFT: X API. It allows you to manage
    tokens and send HTTP requests to various API endpoints using the appropriate method groups.
    """

    __slots__ = ("_http", "_tokens")

    def __init__(self, tokens: Token | Collection[Token], server: Server) -> None:
        self._http = APISession(server)
        self._tokens = self._unpack(tokens)

    def _unpack(self, tokens) -> dict[TokenType, str]:
        stored = {}
        tokens = [tokens] if isinstance(tokens, Token) else tokens
        for token in tokens:
            stored[token.type] = token.value

        return stored

    def get_token(self, type: TokenType) -> str:
        """Retrieves a token of the specified type from the stored tokens.

        Args:
            type (TokenType): The type of the token to retrieve.

        Returns:
            str: The token value corresponding to the specified type.

        Raises:
            MissingTokenError: If no token of the specified type is found.
        """
        try:
            return self.__api_tokens[type]
        except KeyError:
            raise MissingTokenError(type=type)

    def __getattribute__(self, name: str) -> Any:
        try:
            return super().__getattribute__(name)
        except AttributeError:
            return MethodsGroupFabric(group=name, tokens=self._tokens, http=self.http)
