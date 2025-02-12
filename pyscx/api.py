from typing import Any, Collection

from .http import APISession, Server
from .methods import MethodsGroupFabric
from .token import Token, TokenType
from .exceptions import MissingTokenError


class API:
    """API Object Class."""

    __slots__ = ("http", "_tokens")

    def __init__(self, tokens: Token | Collection[Token], server: Server) -> None:
        self.http = APISession(server)
        self._tokens = self._unpack(tokens)

    def _unpack(self, tokens) -> dict[TokenType, str]:
        stored = {}
        tokens = [tokens] if isinstance(tokens, Token) else tokens
        for token in tokens:
            stored[token.type] = token.value

        return stored

    def get_token(self, type: TokenType) -> str:
        try:
            return self.__api_tokens[type]
        except KeyError:
            raise MissingTokenError(type=type)

    def __getattribute__(self, name: str) -> Any:
        try:
            return super().__getattribute__(name)
        except AttributeError:
            return MethodsGroupFabric(group=name, tokens=self._tokens, http=self.http)
