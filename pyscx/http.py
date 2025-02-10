import requests


class APISession(requests.Session):
    """Custom wrapper around the Session class from the `requests` module.

    Allows storing the base URL of the server and sending requests by
    specifying only the resource path.
    """

    def __init__(self, server_url: str):
        super().__init__()
        self.base_url = server_url.rstrip("/")

    def request(self, method, url, *args, **kwargs):
        full_url = f"{self.base_url}/{url.lstrip('/')}"
        return super().request(method, full_url, *args, **kwargs)
