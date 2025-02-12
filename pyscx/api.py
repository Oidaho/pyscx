from enum import Enum

from .http import APISession
from .token import Token, TokenType
from typing import Collection, Type

from .methods import (
    APIMethodGroup,
    RegionsGroup,
    EmissionsGroup,
    FriendsGroup,
    AuctionGroup,
    CharactersGroup,
    ClansGroup,
)


class Server(Enum):
    """List of available STALCRAFT: X API servers"""

    DEMO = "dapi"
    PRODUCTION = "eapi"


class BaseAPI(object):
    """Base API Class for STALCRAFT: X.

    This class serves as the foundation for interacting with the STALCRAFT: X API.
    It provides essential methods and utilities required for configuring and initializing API object.
    """

    def __init__(self, server: Server | str = "dapi") -> None:
        if isinstance(server, Server):
            self.server = server.value
        elif server in Server:
            self.server = server
        else:
            raise ValueError(f"Invalid server value: '{server}'.")

        self.session = self.__make_session()

    def __make_session(self) -> APISession:
        session = APISession(self.server_url)
        session.headers.update(
            {
                "Content-Type": "application/json",
                "User-Agent": "pyscx/1.0.0 (+https://github.com/Oidaho/pyscx)",
                "Accept": "application/json",
            }
        )
        return session

    @property
    def server_url(self) -> str:
        """Returns the URL of the current STALCRAFT: X API server.

        Returns:
            str: The API server URL.
        """
        return f"https://{self.server}.stalcraft.net/"


class API(BaseAPI):
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

    regions: RegionsGroup
    emissions: EmissionsGroup
    friends: FriendsGroup
    auction: AuctionGroup
    characters: CharactersGroup
    clans: ClansGroup

    def __init__(self, tokens: Token | Collection[Token], server: Server | str = "dapi") -> None:
        super().__init__(server=server)
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
            setattr(self, name, group_class(session=self.session, tokens=self.__api_tokens))
