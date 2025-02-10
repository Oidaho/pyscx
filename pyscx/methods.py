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
    """Base class for groups of request methods in the STALCRAFT: X API.

    This class enables the execution of API requests by wrapping the received data into API objects.
    It also provides mechanisms for passing API access keys to the methods and tracking request limits.
    Key features include:

    - Data Wrapping: Automatically wraps the raw data received from API responses into structured API objects,
                    making it easier to work with the results.
    - Access Key Management: Facilitates the secure and efficient passing of API access keys to individual request
                    methods, ensuring proper authentication for each call.
    - Rate Limits Tracking: Implements a system to monitor and manage API request limits, helping developers avoid
                    exceeding allowed quotas and handling rate-limiting scenarios effectively.

    By combining these functionalities, this base class simplifies the process of interacting with the STALCRAFT: X API,
    providing a robust foundation for building higher-level request method groups.
    """

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
    def __extract_nested(
        data: dict[str, Any], nested: str
    ) -> list[dict[str, Any]] | dict[str, Any]:
        if isinstance(data, dict) and nested in data:
            return data[nested]
        return data

    # If there is a need to wrap it in an APIObject
    @staticmethod
    def __wrap_data(
        data: dict[str, Any], model: APIObject
    ) -> APIObject | list[APIObject] | dict[str, Any]:
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
    def get_all(self, **kwargs) -> list[Region]:
        """Retrieves a list of all available regions from the STALCRAFT: X API.

        **Available for execution without an API token.**

        This method sends a GET request to the `/regions` endpoint and returns a list of `Region` objects,
        each representing a game region. The raw response data is automatically parsed and wrapped into
        `Region` instances for easier access and manipulation.

        Args:
            **kwargs: Additional keyword arguments, including query parameters for the request.

        Returns:
            list[Region]: A list of `Region` objects containing information about all available game regions.

        Example:
            ```python
            regions = api.regions.get_all()
            for region in regions:
                print(region.name)
            ```
        """
        path = "/regions"
        return self._request(path=path, model=Region)


class EmissionsGroup(APIMethodGroup):
    @APIMethodGroup._pass_token(TokenType.APPLICATION)
    def get_info(self, region: str, **kwargs) -> Emission:
        """Retrieves detailed information about the emission for a specified region.

        **A token of the following type is required: `TokenType.APPLICATION`.**

        This method sends a GET request to the `/emission` endpoint and returns an `Emission` object containing
        data about the current emission in the specified region. The method requires the `region` parameter and
        uses an API token for authentication.

        Args:
            region (str): The identifier of the game region for which emission data is requested.
            **kwargs: Additional keyword arguments, including query parameters for the request.

        Returns:
            Emission: An object representing the emission data for the specified region.

        Example:
            ```python
            emission = api.emissions.get_info(region="EU")
            print(emission.current_start)
            ```
        """
        path = "/emission"
        token = kwargs.get("token")
        return self._request(path=path, region=region, model=Emission, token=token)


class FriendsGroup(APIMethodGroup):
    @APIMethodGroup._pass_token(TokenType.USER)
    def get_all(self, region: str, character_name: str, **kwargs) -> list[str]:
        """Retrieves a list of all friends for a specified character in a given region.

        **A token of the following type is required: `TokenType.USER`.**

        This method sends a GET request to the `/friends/{character_name}` endpoint and returns
        a list of friend names as strings. The method requires both the `region` and `character_name`
        parameters, and it uses an API token for authentication.

        Args:
            region (str): The identifier of the game region where the character is located.
            character_name (str): The name of the character whose friends list is being retrieved.
            **kwargs: Additional keyword arguments, including query parameters for the request.

        Returns:
            list[str]: A list of strings representing the names of the character's friends.

        Example:
            ```python
            friends = api.friends.get_all(region="EU", character_name="Test-1")
            for friend in friends:
                print(friend)
            ```
        """
        path = f"/friends/{character_name}"
        token = kwargs.get("token")
        return self._request(path=path, region=region, token=token)


class AuctionGroup(APIMethodGroup):
    @APIMethodGroup._pass_token(TokenType.APPLICATION)
    def get_item_history(self, region: str, item_id: str, **kwargs) -> list[AuctionRedeemedLot]:
        """Retrieves the auction history of a specific item in a given region.

        **A token of the following type is required: `TokenType.APPLICATION`.**

        This method sends a GET request to the `/auction/{item_id}/history` endpoint and returns a list of
        `AuctionRedeemedLot` objects, each representing a redeemed lot for the specified item. The raw
        response data is parsed, and nested data under the `"prices"` attribute is extracted and wrapped
        into `AuctionRedeemedLot` instances.

        Args:
            region (str): The identifier of the game region where the auction history is being retrieved.
            item_id (str): The unique identifier of the item for which the auction history is requested.
            **kwargs: Additional keyword arguments, including query parameters for the request.

        Returns:
            list[AuctionRedeemedLot]: A list of `AuctionRedeemedLot` objects representing the auction
                                history of the specified item.

        Example:
            ```python
            history = api.auction.get_item_history(region="EU", item_id="1kv2")
            for lot in history:
                print(lot.price)
            ```
        """
        path = f"/auction/{item_id}/history"
        token = kwargs.get("token")
        nested_attr = "prices"
        return self._request(
            path=path, region=region, model=AuctionRedeemedLot, nested=nested_attr, token=token
        )

    @APIMethodGroup._pass_token(TokenType.APPLICATION)
    def get_item_lots(self, region: str, item_id: str, **kwargs) -> list[AuctionLot]:
        """Retrieves a list of active auction lots for a specific item in a given region.

        **A token of the following type is required: `TokenType.APPLICATION`.**

        This method sends a GET request to the `/auction/{item_id}/lots` endpoint and returns a list of `AuctionLot` objects,
        each representing an active lot for the specified item. The raw response data is parsed, and nested data under the `"lots"`
        attribute is extracted and wrapped into `AuctionLot` instances.

        Args:
            region (str): The identifier of the game region where the auction lots are being retrieved.
            item_id (str): The unique identifier of the item for which the auction lots are requested.
            **kwargs: Additional keyword arguments, including query parameters for the request.

        Returns:
            list[AuctionLot]: A list of `AuctionLot` objects representing the active auction lots for the specified item.

        Example:
            ```python
            lots = api.auction.get_item_lots(region="eu", item_id="1kv2")
            for lot in lots:
                print(lot.current_price)
            ```
        """
        path = f"/auction/{item_id}/lots"
        token = kwargs.get("token")
        nested_attr = "lots"
        return self._request(
            path=path, region=region, model=AuctionLot, nested=nested_attr, token=token
        )


class CharactersGroup(APIMethodGroup):
    @APIMethodGroup._pass_token(TokenType.USER)
    def get_all(self, region: str, **kwargs) -> list[CharacterInfo]:
        """Retrieves a list of all characters in a specified region.

        **A token of the following type is required: `TokenType.USER`.**

        This method sends a GET request to the `/characters` endpoint and returns a list of `CharacterInfo`
        objects, each representing a game character in the specified region. The raw response data is
        parsed and wrapped into `CharacterInfo` instances for easier access and manipulation.

        Args:
            region (str): The identifier of the game region for which character data is requested.
            **kwargs: Additional keyword arguments, including query parameters for the reques.

        Returns:
            list[CharacterInfo]: A list of `CharacterInfo` objects containing information about all characters
                            in the specified region.

        Example:
            ```python
            characters = api.characters.get_all(region="EU")
            for character in characters:
                print(character.name)
            ```
        """
        path = "/characters"
        token = kwargs.get("token")
        return self._request(path=path, region=region, model=CharacterInfo, token=token)

    @APIMethodGroup._pass_token(TokenType.APPLICATION)
    def get_profile(self, region: str, character_name: str, **kwargs) -> FullCharacterInfo:
        """Retrieves the full profile information of a specific character.

        **A token of the following type is required: `TokenType.APPLICATION`.**

        This method sends a GET request to the `/character/by-name/{character_name}/profile`
        endpoint and returns a `FullCharacterInfo` object containing detailed information about
        the specified character. The raw response data is parsed and wrapped into a `FullCharacterInfo`
        instance for easier access and manipulation.

        Args:
            region (str): The identifier of the game region where the character is located.
            character_name (str): The name of the character whose profile is being retrieved.
            **kwargs: Additional keyword arguments, including query parameters for the request.

        Returns:
            FullCharacterInfo: An object representing the full profile information of the specified character.

        Example:
            ```python
            profile = api.characters.get_profile(region="EU", character_name="Test-1")
            print(profile.name)
            print(profile.stat.level)
            ```
        """
        path = f"/character/by-name/{character_name}/profile"
        token = kwargs.get("token")
        return self._request(path=path, region=region, model=FullCharacterInfo, token=token)


class ClansGroup(APIMethodGroup):
    @APIMethodGroup._pass_token(TokenType.APPLICATION)
    def get_info(self, region: str, clan_id: str, **kwargs) -> Clan:
        """Retrieves detailed information about a specific clan.

        **A token of the following type is required: `TokenType.APPLICATION`.**

        This method sends a GET request to the `/clan/{clan_id}/info` endpoint and returns a `Clan`
        object containing detailed information about the specified clan. The raw response data
        is parsed and wrapped into a `Clan` instance for easier access and manipulation.

        Args:
            region (str): The identifier of the game region where the clan is located.
            clan_id (str): The unique identifier of the clan for which information is requested.
            **kwargs: Additional keyword arguments, including query parameters for the request.

        Returns:
            Clan: An object representing the detailed information of the specified clan.

        Example:
            ```python
            clan = api.clans.get_info(region="EU", clan_id="647d6c53-b3d7-4d30-8d08-de874eb1d845")
            print(clan.name)
            print(clan.member_count)
            ```
        """
        path = f"/clan/{clan_id}/info"
        token = kwargs.get("token")
        return self._request(path=path, region=region, model=Clan, token=token)

    @APIMethodGroup._pass_token(TokenType.USER)
    def get_members(self, region: str, clan_id: str, **kwargs) -> list[ClanMember]:
        """Retrieves a list of all members in a specific clan.

        **A token of the following type is required: `TokenType.APPLICATION`.**

        This method sends a GET request to the `/clan/{clan_id}/members` endpoint and returns a list
        of `ClanMember` objects, each representing a member of the specified clan. The raw response
        data is parsed and wrapped into `ClanMember` instances for easier access and manipulation.

        Args:
            region (str): The identifier of the game region where the clan is located.
            clan_id (str): The unique identifier of the clan for which member data is requested.
            **kwargs: Additional keyword arguments, including query parameters for the request.

        Returns:
            list[ClanMember]: A list of `ClanMember` objects representing the members of the specified clan.

        Example:
            ```python
            members = api.clans.get_members(region="EU", clan_id="647d6c53-b3d7-4d30-8d08-de874eb1d845")
            for member in members:
                print(member.name)
                print(member.rank)
            ```
        """
        path = f"/clan/{clan_id}/members"
        token = kwargs.get("token")
        return self._request(path=path, region=region, model=ClanMember, token=token)

    @APIMethodGroup._pass_token(TokenType.APPLICATION)
    def get_all(self, region: str, **kwargs) -> list[Clan]:
        """Retrieves a list of all clans in a specified region.

        **A token of the following type is required: `TokenType.APPLICATION`.**

        This method sends a GET request to the `/clans` endpoint and returns a list of `Clan`
        objects, each representing a clan in the specified region. The raw response data is
        parsed, and nested data under the `"data"` attribute is extracted and wrapped into
        `Clan` instances for easier access and manipulation.

        Args:
            region (str): The identifier of the game region for which clan data is requested.
            **kwargs: Additional keyword arguments, including query parameters for the request.

        Returns:
            list[Clan]: A list of `Clan` objects containing information about all clans in the
                            specified region.

        Example:
            ```python
            clans = api.clans.get_all(region="EU")
            for clan in clans:
                print(clan.name)
                print(clan.member_count)
            ```
        """
        path = "/clans"
        token = kwargs.get("token")
        nested_attr = "data"
        return self._request(path=path, region=region, model=Clan, token=token, nested=nested_attr)
