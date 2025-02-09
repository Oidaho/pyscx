from functools import wraps
from .http import APISession
from .token import TokenType
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
    def __init__(self, session: APISession, tokens: dict[TokenType, str]):
        self.session = session
        self.tokens = tokens

    def _request(
        self, path: str, region: str = "", token: str | None = None, model: APIObject | None = None
    ) -> list[APIObject] | APIObject:
        request_path = f"{region}/{path.lstrip('/')}"
        response = self.session.request(
            method="GET",
            url=request_path,
            headers={"Authorization": f"Bearer {token}"} if token else {},
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

    @classmethod
    def _pass_token(cls, token_type: TokenType) -> callable:
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                token = self.tokens.get(token_type)
                if token is None:
                    raise PermissionError(
                        f"This method is only available with a token of the type '{token_type}'. "
                        "This type of token was not passed to the API."
                    )
                result = func(self, *args, token=token, **kwargs)
                return result

            return wrapper

        return decorator


class RegionsGroup(APIMethodGroup):
    def get_all(self) -> list[Region]:
        path = "/regions"
        return self._request(path, model=Region)


class EmissionsGroup(APIMethodGroup):
    @APIMethodGroup._pass_token(TokenType.APPLICATION)
    def get_info(self, region: str, **kwargs) -> Emission:
        path = "/emission"
        token = kwargs.get("token")
        return self._request(path, region, token, Emission)


class FriendsGroup(APIMethodGroup):
    @APIMethodGroup._pass_token(TokenType.USER)
    def get_all(self, region: str, character_name: str, **kwargs) -> list[str]:
        path = f"/friends/{character_name}"
        token = kwargs.get("token")
        return self._request(path, region, token)


class AuctionGroup(APIMethodGroup):
    @APIMethodGroup._pass_token(TokenType.APPLICATION)
    def get_item_history(self, region: str, item_id: str, **kwargs) -> list[AuctionRedeemedLot]:
        path = f"/auction/{item_id}/history"
        token = kwargs.get("token")
        return self._request(path, region, token, AuctionRedeemedLot)

    @APIMethodGroup._pass_token(TokenType.APPLICATION)
    def get_item_lots(self, region: str, item_id: str, **kwargs) -> list[AuctionLot]:
        path = f"/auction/{item_id}/lots"
        token = kwargs.get("token")
        return self._request(path, region, token, AuctionLot)


class CharactersGroup(APIMethodGroup):
    @APIMethodGroup._pass_token(TokenType.USER)
    def get_all(self, region: str, **kwargs) -> list[CharacterInfo]:
        path = "/characters"
        token = kwargs.get("token")
        return self._request(path, region, token, CharacterInfo)

    @APIMethodGroup._pass_token(TokenType.APPLICATION)
    def get_profile(self, region: str, character_name: str, **kwargs) -> FullCharacterInfo:
        path = f"/character/by-name/{character_name}/profile"
        token = kwargs.get("token")
        return self._request(path, region, token, FullCharacterInfo)


class ClansGroup(APIMethodGroup):
    @APIMethodGroup._pass_token(TokenType.APPLICATION)
    def get_info(self, region: str, clan_id: str, **kwargs) -> Clan:
        path = f"/clan/{clan_id}/info"
        token = kwargs.get("token")
        return self._request(path, region, token, Clan)

    @APIMethodGroup._pass_token(TokenType.USER)
    def get_members(self, region: str, clan_id: str, **kwargs) -> list[ClanMember]:
        path = f"/clan/{clan_id}/members"
        token = kwargs.get("token")
        return self._request(path, region, token, ClanMember)

    @APIMethodGroup._pass_token(TokenType.APPLICATION)
    def get_all(self, region: str, **kwargs) -> list[Clan]:
        path = "/clans"
        token = kwargs.get("token")
        return self._request(path, region, token, Clan)
