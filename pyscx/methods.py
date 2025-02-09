from .http import APISession

from .objects import (
    Region,
    Emission,
    AuctionRedeemedLot,
    AuctionLot,
    CharacterInfo,
    FullCharacterInfo,
    Clan,
    ClanMember,
)


class APIMethodGroup(object):
    def __init__(self, session: APISession):
        self.session = session


class RegionsGroup(APIMethodGroup):
    def get_all(self) -> list[Region]:
        request_path = "/regions"
        response = self.session.request(method="GET", url=request_path)

        region_list = [Region(**region_data) for region_data in response.json()]
        return region_list


class EmissionsGroup(APIMethodGroup):
    def get_info(self, region: str, token: str) -> Emission:
        request_path = f"/{region}/emission"
        response = self.session.request(
            method="GET",
            url=request_path,
            headers={"Authorization": f"Bearer {token}"},
        )

        return Emission(**response.json())


class FriendsGroup(APIMethodGroup):
    def get_all(self, region: str, character_name: str, token: str) -> list[str]:
        request_path = f"/{region}/friends/{character_name}"
        response = self.session.request(
            method="GET",
            url=request_path,
            headers={"Authorization": f"Bearer {token}"},
        )

        return response.json()
