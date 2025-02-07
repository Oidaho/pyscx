from enum import Enum

import requests
from cachetools import TTLCache, cached

from .region import Region

# Caching the results of accessing query interfaces
short_cache = TTLCache(maxsize=100, ttl=2)
long_cahce = TTLCache(maxsize=10, ttl=3600)


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
            raise ValueError(
                f"Invalid server value: {server}. Expected an instance of 'Server' or 'str'."
            )

        self.session = self.__make_session()

    def get_server_url(self) -> str:
        """Returns the URL of the current STALCRAFT: X API server.

        Returns:
            str: API server URL
        """
        return f"https://{self.server}.stalcraft.net/"

    def __make_session(self) -> requests.Session:
        session = requests.Session()
        session.headers.update({"Content-Type": "application/json"})
        return session

    @cached(long_cahce)
    def get_regions(self) -> list[Region]:
        url = self.get_server_url() + "regions"
        response = self.session.get(url)
        return [Region(**region_data) for region_data in response.json()]


class UserAPI(API):
    pass


class ApplicationAPI(API):
    pass
