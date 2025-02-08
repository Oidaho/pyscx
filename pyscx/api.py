from enum import Enum

from .http import APISession


class Server(Enum):
    """List of available STALCRAFT: X API servers"""

    DEMO = "dapi"
    PRODUCTION = "eapi"


class API(object):
    """Base API class for STALCRAFT:X.
    Includes API configuration methods and interfaces
    for executing requests that neither require an
    authorization key nor depend on a specific region.
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

    regions: any = ...


class UserAPI(API):
    def __init__(self, user_token: str, server: Server | str = "dapi") -> None:
        super().__init__(server=server)
        self.session.include_token(token=user_token)

    friends: any = ...
    characters: any = ...
    clan: any = ...


class ApplicationAPI(API):
    def __init__(self, application_token: str, server: Server | str = "dapi") -> None:
        super().__init__(server=server)
        self.session.include_token(token=application_token)

    emission: any = ...
    character: any = ...
    clans: any = ...
    auction: any = ...
