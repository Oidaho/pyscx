import requests


class APISession(requests.Session):
    def __init__(self, server_url: str):
        super().__init__()
        self.base_url = server_url.rstrip("/")

    def request(self, method, url, *args, **kwargs):
        full_url = f"{self.base_url}/{url.lstrip('/')}"
        return super().request(method, full_url, *args, **kwargs)
