from __future__ import annotations

from functools import wraps

from .exceptions import MissingTokenError, InvalidMethodGroup
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


class MethodsGroup:
    __slots__ = ("region", "_http", "_tokens")

    def __init__(self, region: str | None, session: APISession, tokens: dict[TokenType, str]):
        self._http = session
        self._tokens = tokens
        self.region = region

    @staticmethod
    def wrap_data(data: dict | list[dict], model: APIObject) -> APIObject:
        if isinstance(data, list):
            return [model(**item) for item in data]
        return model(**data)

    @classmethod
    def _required_token(cls, token_type: TokenType) -> callable:
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                token = kwargs.pop("token", None)
                if not token:
                    try:
                        token = self._tokens[token_type]
                    except KeyError:
                        raise MissingTokenError(
                            f"This method requires an access token of type '{token_type}' to complete the request."
                        )

                return func(self, token=token, *args, **kwargs)

            return wrapper

        return decorator

    @property
    def group_name(self) -> str:
        print(type(self).__name__)
        return type(self).__name__.replace("Methods", "").lower()


class RegionsMethods(MethodsGroup):
    def get_all(self, **kwargs) -> list[Region]:
        resource = f"/{self.group_name}"
        response = self._http.get(url=resource)
        return response


class EmissionsMethods(MethodsGroup):
    @MethodsGroup._required_token(TokenType.APPLICATION)
    def get_info(self, **kwargs) -> Emission:
        resource = f"{self.region}/{self.group_name[:-1]}"
        headers = {"Authorization": f"Bearer {kwargs.pop('token')}"}
        response = self._http.get(url=resource, headers=headers)
        return self.wrap_data(response.json(), Emission)


class FriendsMethods(MethodsGroup):
    @MethodsGroup._required_token(TokenType.USER)
    def get_all(self, character_name: str, **kwargs) -> list[str]:
        resource = f"{self.region}/{self.group_name}/{character_name}"
        headers = {"Authorization": f"Bearer {kwargs.pop('token')}"}
        response = self._http.get(url=resource, headers=headers)
        return response.json()


class AuctionMethods(MethodsGroup):
    @MethodsGroup._required_token(TokenType.APPLICATION)
    def get_item_history(self, item_id: str, **kwargs) -> list[AuctionRedeemedLot]:
        resource = f"{self.region}/{self.group_name}/{item_id}/history"
        headers = {"Authorization": f"Bearer {kwargs.pop('token')}"}
        response = self._http.get(url=resource, headers=headers, params=kwargs)
        return self.wrap_data(response.json()["prices"], AuctionRedeemedLot)

    @MethodsGroup._required_token(TokenType.APPLICATION)
    def get_item_lots(self, item_id: str, **kwargs) -> list[AuctionLot]:
        resource = f"{self.region}/{self.group_name}/{item_id}/lots"
        headers = {"Authorization": f"Bearer {kwargs.pop('token')}"}
        response = self._http.get(url=resource, headers=headers, params=kwargs)
        return self.wrap_data(response.json()["lots"], AuctionLot)


class CharactersMethods(MethodsGroup):
    @MethodsGroup._required_token(TokenType.USER)
    def get_all(self, **kwargs) -> list[CharacterInfo]:
        resource = f"{self.region}/{self.group_name}"
        headers = {"Authorization": f"Bearer {kwargs.pop('token')}"}
        response = self._http.get(url=resource, headers=headers, params=kwargs)
        return self.wrap_data(response.json(), CharacterInfo)

    @MethodsGroup._required_token(TokenType.APPLICATION)
    def get_profile(self, character_name: str, **kwargs) -> FullCharacterInfo:
        resource = f"{self.region}/{self.group_name[:-1]}/by-name/{character_name}/profile"
        headers = {"Authorization": f"Bearer {kwargs.pop('token')}"}
        response = self._http.get(url=resource, headers=headers, params=kwargs)
        return self.wrap_data(response.json(), FullCharacterInfo)


class ClansMethods(MethodsGroup):
    @MethodsGroup._required_token(TokenType.APPLICATION)
    def get_info(self, clan_id: str, **kwargs) -> Clan:
        resource = f"{self.region}/{self.group_name[:-1]}/{clan_id}/info"
        headers = {"Authorization": f"Bearer {kwargs.pop('token')}"}
        response = self._http.get(url=resource, headers=headers, params=kwargs)
        return self.wrap_data(response.json(), Clan)

    @MethodsGroup._required_token(TokenType.USER)
    def get_members(self, clan_id: str, **kwargs) -> list[ClanMember]:
        resource = f"{self.region}/{self.group_name[:-1]}/{clan_id}/members"
        headers = {"Authorization": f"Bearer {kwargs.pop('token')}"}
        response = self._http.get(url=resource, headers=headers, params=kwargs)
        return self.wrap_data(response.json(), ClanMember)

    @MethodsGroup._required_token(TokenType.APPLICATION)
    def get_all(self, **kwargs) -> list[Clan]:
        resource = f"{self.region}/{self.group_name}"
        headers = {"Authorization": f"Bearer {kwargs.pop('token')}"}
        response = self._http.get(url=resource, headers=headers, params=kwargs)
        return self.wrap_data(response.json()["data"], Clan)


class MethodsGroupFabric:
    __slots__ = ("_group_class", "_tokens", "_http")

    _method_groups = {
        "regions": RegionsMethods,
        "emissions": EmissionsMethods,
        "friends": FriendsMethods,
        "auction": AuctionMethods,
        "characters": CharactersMethods,
        "clans": ClansMethods,
    }

    def __init__(self, group: str, http: APISession, tokens: dict[TokenType, str]) -> None:
        try:
            self._group_class = self._method_groups[group]
            self._tokens = tokens
            self._http = http
        except KeyError:
            raise InvalidMethodGroup(group=group)

    def __call__(self, region: str | None = None) -> MethodsGroup:
        return self._group_class(region, self._http, self._tokens)
