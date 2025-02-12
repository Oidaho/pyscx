from enum import Enum

import requests

DEFAULT_AGENT = "pyscx/1.0.0 (+https://github.com/Oidaho/pyscx)"


class Server(Enum):
    """List of available STALCRAFT: X API servers"""

    DEMO = "dapi"
    PRODUCTION = "eapi"


class APISession(requests.Session):
    """Custom wrapper around the Session class from the `requests` module.

    Allows storing the base URL of the server and sending requests by
    specifying only the resource path.
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
        """Returns the URL of the current STALCRAFT: X API server.

        Returns:
            str: The API server URL.
        """
        return f"https://{self.server.value}.stalcraft.net"
