from .http import APISession

from .objects import Region, Emission


class APIMethodGroup(object):
    def __init__(self, session: APISession):
        self.session = session


class RegionsMethods(APIMethodGroup):
    def get(self) -> list[Region]:
        response = self.session.request(method="GET", url="/regions")
        return [Region(**region_data) for region_data in response.json()]


class EmissionsMethods(APIMethodGroup):
    def get(self, region: str) -> Emission:
        response = self.session.request(method="GET", url=f"/{region}/emission")
        return Emission(**response.json())
