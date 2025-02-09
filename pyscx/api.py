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
    """Base API class for STALCRAFT:X.
    Includes API configuration methods.
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
            str: API server URL
        """
        return f"https://{self.server}.stalcraft.net/"


class API(BaseAPI):
    __api_tokens: dict[TokenType, str] = {}

    regions: RegionsGroup
    emissions: EmissionsGroup
    friends: FriendsGroup
    auction: AuctionGroup
    characters: CharactersGroup
    clans: ClansGroup

    def __init__(self, tokens: Token | Collection[Token], server: Server | str = "dapi") -> None:
        super().__init__(server=server)

        # * Guarantee of the existence of the token
        for type in TokenType:
            self.__api_tokens[type] = None

        tokens = [tokens] if isinstance(tokens, Token) else tokens
        for token in tokens:
            try:
                self.__api_tokens[token.type] = token.value
            except KeyError:
                raise ValueError("Passed token with unxecepted type.")

        # Initializing the API methods
        self.__init_methods__()

    def __getattr__(self, name):
        try:
            # Default __getattr__
            return super().__getattr__(name)

        except AttributeError as e:
            # Getting token as a class attribute
            postfix = "_token"
            if name.endswith(postfix):
                token_type = name.rstrip(postfix)
                token = self.__api_tokens.get(TokenType(token_type))

                if token is None:
                    raise AttributeError(
                        f"{self.__class__.__name__} object has no attribute '{name}'"
                    )

                return token

            raise AttributeError(e)

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
