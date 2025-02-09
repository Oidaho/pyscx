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


class AuctionGroup(APIMethodGroup):
    def get_item_history(self, region: str, item_id: str, token: str) -> list[AuctionRedeemedLot]:
        request_path = f"/{region}/auction/{item_id}/history"
        response = self.session.request(
            method="GET",
            url=request_path,
            headers={"Authorization": f"Bearer {token}"},
        )

        history = [AuctionRedeemedLot(**lot_data) for lot_data in response.json()["prices"]]
        return history

    def get_item_lots(self, region: str, item_id: str, token: str) -> list[AuctionLot]:
        request_path = f"/{region}/auction/{item_id}/lots"
        response = self.session.request(
            method="GET",
            url=request_path,
            headers={"Authorization": f"Bearer {token}"},
        )

        lots = [AuctionLot(**lot_data) for lot_data in response.json()["lots"]]
        return lots


class CharactersGroup(APIMethodGroup):
    def get_all(self, region: str, token: str) -> list[CharacterInfo]:
        request_path = f"/{region}/characters"
        response = self.session.request(
            method="GET",
            url=request_path,
            headers={"Authorization": f"Bearer {token}"},
        )

        сcharacters_list = [CharacterInfo(**data) for data in response.json()]
        return сcharacters_list

    def get_profile(self, region: str, character_name: str, token: str) -> FullCharacterInfo:
        request_path = f"/{region}/character/by-name/{character_name}/profile"
        response = self.session.request(
            method="GET",
            url=request_path,
            headers={"Authorization": f"Bearer {token}"},
        )

        return FullCharacterInfo(**response.json())


class ClansGroup(APIMethodGroup):
    def get_info(self, region: str, clan_id: str, token: str) -> Clan:
        request_path = f"{region}/clan/{clan_id}/info"
        response = self.session.request(
            method="GET",
            url=request_path,
            headers={"Authorization": f"Bearer {token}"},
        )

        return Clan(**response.json())

    def get_members(self, region: str, clan_id: str, token: str) -> list[ClanMember]:
        request_path = f"{region}/clan/{clan_id}/members"
        response = self.session.request(
            method="GET",
            url=request_path,
            headers={"Authorization": f"Bearer {token}"},
        )

        clan_members = [ClanMember(**data) for data in response.json()]
        return clan_members

    def get_all(self, region: str, token: str) -> list[Clan]:
        request_path = f"{region}/clans"
        response = self.session.request(
            method="GET",
            url=request_path,
            headers={"Authorization": f"Bearer {token}"},
        )

        clan_list = [Clan(**data) for data in response.json()]
        return clan_list
