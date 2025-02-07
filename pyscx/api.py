from enum import Enum

import requests


class Server(Enum):
    """List of available STALCRAFT: X API servers"""

    DEMO = "dapi"
    PRODUCTION = "eapi"


class API(object):
    def __init__(self, server: Server | str = "dapi") -> None:
        if isinstance(server, Server):
            self.server = server.value
        elif server in Server:
            self.server = server
        else:
            # TODO: message
            raise ValueError()

        self.session = self.make_session()

    def get_server_url(self) -> str:
        """Returns the URL of the current STALCRAFT: X API server.

        Returns:
            str: API server URL
        """
        return f"https://{self.server}.stalcraft.net/"

    def make_session(self) -> requests.Session:
        session = requests.Session()
        return session


class UserAPI(API):
    pass


class ApplicationAPI(API):
    pass
