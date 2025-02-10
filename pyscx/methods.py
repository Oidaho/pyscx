from functools import wraps
from typing import Any

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
from .token import TokenType


class APIMethodGroup(object):
    def __init__(self, session: APISession, tokens: dict[TokenType, str]):
        self.session = session
        self.tokens = tokens

    def _request(
        self,
        path: str,
        region: str = "",
        model: APIObject | None = None,
        nested: str | None = None,
        token: str | None = None,
        query_params: dict | None = None,
    ) -> list[APIObject] | APIObject:
        request_path = f"{region}/{path.lstrip('/')}"
        response = self.session.request(
            method="GET",
            url=request_path,
            headers={"Authorization": f"Bearer {token}"} if token else {},
            params=query_params,
        )
        response.raise_for_status()

        data = self.__extract_nested(response.json(), nested)
        return self.__wrap_data(data, model)

    # Targeted extraction of a nested structure
    @staticmethod
    def __extract_nested(data: dict[str, Any], nested: str) -> list[dict] | dict:
        if isinstance(data, dict) and nested in data:
            return data[nested]
        return data

    # If there is a need to wrap it in an APIObject
    @staticmethod
    def __wrap_data(data: dict[str, Any], model: APIObject) -> APIObject:
        if model:
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

        return self._request(
            path=path,
            model=Region,
        )


class EmissionsGroup(APIMethodGroup):
    @APIMethodGroup._pass_token(TokenType.APPLICATION)
    def get_info(self, region: str, **kwargs) -> Emission:
        path = "/emission"
        token = kwargs.get("token")

        return self._request(
            path=path,
            region=region,
            model=Emission,
            token=token,
        )


class FriendsGroup(APIMethodGroup):
    @APIMethodGroup._pass_token(TokenType.USER)
    def get_all(self, region: str, character_name: str, **kwargs) -> list[str]:
        path = f"/friends/{character_name}"
        token = kwargs.get("token")

        return self._request(
            path=path,
            region=region,
            token=token,
        )


class AuctionGroup(APIMethodGroup):
    @APIMethodGroup._pass_token(TokenType.APPLICATION)
    def get_item_history(self, region: str, item_id: str, **kwargs) -> list[AuctionRedeemedLot]:
        path = f"/auction/{item_id}/history"
        token = kwargs.get("token")
        nested_attr = "prices"

        return self._request(
            path=path,
            region=region,
            model=AuctionRedeemedLot,
            nested=nested_attr,
            token=token,
        )

    @APIMethodGroup._pass_token(TokenType.APPLICATION)
    def get_item_lots(self, region: str, item_id: str, **kwargs) -> list[AuctionLot]:
        path = f"/auction/{item_id}/lots"
        token = kwargs.get("token")
        nested_attr = "lots"

        return self._request(
            path=path,
            region=region,
            model=AuctionLot,
            nested=nested_attr,
            token=token,
        )


class CharactersGroup(APIMethodGroup):
    @APIMethodGroup._pass_token(TokenType.USER)
    def get_all(self, region: str, **kwargs) -> list[CharacterInfo]:
        path = "/characters"
        token = kwargs.get("token")

        return self._request(
            path=path,
            region=region,
            model=CharacterInfo,
            token=token,
        )

    @APIMethodGroup._pass_token(TokenType.APPLICATION)
    def get_profile(self, region: str, character_name: str, **kwargs) -> FullCharacterInfo:
        path = f"/character/by-name/{character_name}/profile"
        token = kwargs.get("token")

        return self._request(
            path=path,
            region=region,
            model=FullCharacterInfo,
            token=token,
        )


class ClansGroup(APIMethodGroup):
    @APIMethodGroup._pass_token(TokenType.APPLICATION)
    def get_info(self, region: str, clan_id: str, **kwargs) -> Clan:
        path = f"/clan/{clan_id}/info"
        token = kwargs.get("token")

        return self._request(
            path=path,
            region=region,
            model=Clan,
            token=token,
        )

    @APIMethodGroup._pass_token(TokenType.USER)
    def get_members(self, region: str, clan_id: str, **kwargs) -> list[ClanMember]:
        path = f"/clan/{clan_id}/members"
        token = kwargs.get("token")

        return self._request(
            path=path,
            region=region,
            model=ClanMember,
            token=token,
        )

    @APIMethodGroup._pass_token(TokenType.APPLICATION)
    def get_all(self, region: str, **kwargs) -> list[Clan]:
        path = "/clans"
        token = kwargs.get("token")
        nested_attr = "data"

        return self._request(
            path=path,
            region=region,
            model=Clan,
            token=token,
            nested=nested_attr,
        )
