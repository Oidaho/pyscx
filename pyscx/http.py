from enum import Enum

import requests

DEFAULT_AGENT = "pyscx/1.1.3 (+https://github.com/Oidaho/pyscx)"


class Server(Enum):
    """Enumeration representing the available STALCRAFT: X API servers.

    Attributes:
        DEMO (str): The demo environment server.
        PRODUCTION (str): The production environment server.
    """

    DEMO = "dapi"
    PRODUCTION = "eapi"


class APISession(requests.Session):
    """Custom wrapper around the Session class from the `requests` module.

    Attributes:
        server (Server): The server environment to be used for API requests.
    """

    def __init__(self, server: Server):
        super().__init__()
        self.server = server

        self.headers["User-Agent"] = DEFAULT_AGENT

    def get(self, url, **kwargs) -> requests.Response:
        full_url = f"{self.server_url}/{url.lstrip('/')}"
        response = super().get(full_url, **kwargs)
        response.raise_for_status()
        return response

    @property
    def server_url(self) -> str:
        """Returns the base URL of the current STALCRAFT: X API server.

        Returns:
            str: The full URL of the current API server.
        """
        return f"https://{self.server.value}.stalcraft.net"
