from .http import APISession
from .objects import (
    APIObject,
    AuctionLot,
    AuctionRedeemedLot,
    CharacterInfo,
    Clan,
    ClanMember,
    Emission,
    FullCharacterInfo,
    Region,
)


class APIMethodGroup(object):
    def __init__(self, session: APISession):
        self.session = session

    def _request(
        self, path: str, region: str = "", token: str | None = None, model: APIObject | None = None
    ) -> list[APIObject] | APIObject:
        request_path = f"{region}/{path.lstrip('/')}"
        response = self.session.request(
            method="GET",
            url=request_path,
            headers={"Authorization": f"Bearer {token}"},
        )
        data = response.json()

        # If there is a need to wrap it in a APIObject
        if model:
            # If data is a list, turn it into a list of APIObject.
            if isinstance(data, list):
                return [model(**item) for item in data]
            return model(**data)
        else:
            return data


class RegionsGroup(APIMethodGroup):
    def get_all(self) -> list[Region]:
        path = "/regions"
        return self._request(path, model=Emission)


class EmissionsGroup(APIMethodGroup):
    def get_info(self, region: str, token: str) -> Emission:
        path = "/emission"
        return self._request(path, region, token, Emission)


class FriendsGroup(APIMethodGroup):
    def get_all(self, region: str, character_name: str, token: str) -> list[str]:
        path = f"friends/{character_name}"
        return self._request(path, region, token)


class AuctionGroup(APIMethodGroup):
    def get_item_history(self, region: str, item_id: str, token: str) -> list[AuctionRedeemedLot]:
        path = f"auction/{item_id}/history"
        return self._request(path, region, token, AuctionRedeemedLot)

    def get_item_lots(self, region: str, item_id: str, token: str) -> list[AuctionLot]:
        path = f"auction/{item_id}/lots"
        return self._request(path, region, token, AuctionLot)


class CharactersGroup(APIMethodGroup):
    def get_all(self, region: str, token: str) -> list[CharacterInfo]:
        path = "characters"
        return self._request(path, region, token, CharacterInfo)

    def get_profile(self, region: str, character_name: str, token: str) -> FullCharacterInfo:
        path = f"character/by-name/{character_name}/profile"
        return self._request(path, region, token, FullCharacterInfo)


class ClansGroup(APIMethodGroup):
    def get_info(self, region: str, clan_id: str, token: str) -> Clan:
        path = f"clan/{clan_id}/info"
        return self._request(path, region, token, Clan)

    def get_members(self, region: str, clan_id: str, token: str) -> list[ClanMember]:
        path = f"clan/{clan_id}/members"
        return self._request(path, region, token, ClanMember)

    def get_all(self, region: str, token: str) -> list[Clan]:
        path = "clans"
        return self._request(path, region, token, Clan)
