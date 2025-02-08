from abc import ABC, abstractmethod
from enum import Enum

from .http import APISession
from .methods import Regions


class Server(Enum):
    """List of available STALCRAFT: X API servers"""

    DEMO = "dapi"
    PRODUCTION = "eapi"


class BaseAPI(ABC):
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

    @abstractmethod
    def __init_api_methods__(self) -> None:
        """_summary_"""
        pass


class API(BaseAPI):
    def __init__(self, server: Server | str = "dapi") -> None:
        super().__init__(server=server)
        self.__init_api_methods__()

    def __init_api_methods__(self) -> None:
        self.regions = Regions(self.session)


class UserAPI(API):
    def __init__(self, user_token: str, server: Server | str = "dapi") -> None:
        super().__init__(server=server)
        self.session.include_token(token=user_token)
        self.__init_api_methods__()

    def __init_api_methods__(self) -> None:
        super().__init_api_methods__()
        self.friends: any = ...
        self.characters: any = ...
        self.clan: any = ...


class ApplicationAPI(API):
    def __init__(self, application_token: str, server: Server | str = "dapi") -> None:
        super().__init__(server=server)
        self.session.include_token(token=application_token)
        self.__init_api_methods__()

    def __init_api_methods__(self) -> None:
        super().__init_api_methods__()
        self.emission: any = ...
        self.character: any = ...
        self.clans: any = ...
        self.auction: any = ...
