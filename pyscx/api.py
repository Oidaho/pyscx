from typing import Collection, Type

from .http import APISession, Server
from .methods import (
    APIMethodGroup,
    AuctionGroup,
    CharactersGroup,
    ClansGroup,
    EmissionsGroup,
    FriendsGroup,
    RegionsGroup,
)
from .token import Token, TokenType


class API:
    """API Object Class.

    This class enables sending requests to the STALCRAFT: X API server.
    To provide a more organized and user-friendly interface, the request
    methods are grouped into categories based on their functionality:

    - Regions: Methods related to retrieving information about game regions.
    - Emissions: Methods for accessing data about emissions within the game.
    - Friends: Methods to manage and retrieve information about friend lists.
    - Auction: Methods for interacting with the in-game auction system, including
                retrieving and purchasing lots.
    - Characters: Methods to obtain detailed information about game characters,
                including statistics and achievements.
    - Clans: Methods for working with clan-related data, such as member lists,
                ranks, and other clan-specific information.

    This structure allows for easier navigation and usage of the API, ensuring that
    developers can quickly find and utilize the methods they need for their specific use cases.
    """

    def __init__(self, tokens: Token | Collection[Token], server: Server) -> None:
        self.http = APISession(server)

        self.__store_tokens(tokens)
        self.__init_methods__()

    def __store_tokens(self, tokens) -> None:
        stored = {}
        tokens = [tokens] if isinstance(tokens, Token) else tokens
        for token in tokens:
            stored[token.type] = token.value
        self.__api_tokens = stored

    def get_token(self, type: TokenType) -> str:
        try:
            return self.__api_tokens[type]
        except KeyError:
            raise  # MissingTokenError

    def __init_methods__(self) -> None:
        method_groups: dict[str, Type[APIMethodGroup]] = {
            "regions": RegionsGroup,
            "emissions": EmissionsGroup,
            "friends": FriendsGroup,
            "auction": AuctionGroup,
            "characters": CharactersGroup,
            "clans": ClansGroup,
        }

        for name, group_class in method_groups.items():
            setattr(self, name, group_class(session=self.http, tokens=self.__api_tokens))
