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
    """A base class for managing method groupsrelated to specific API endpoints.

    The `MethodsGroup` class is responsible for providing common functionality
    to interact with various API method groups (such as regions, emissions, etc.).
    It provides utilities to wrap data into model instances and manage tokens for API requests.

    Attributes:
        region (str | None): The region associated with the method group (optional).
        _http (APISession): The HTTP session object used for making API requests.
        _tokens (dict): A dictionary containing tokens used for authentication.

    Args:
        region (str | None): The region to associate with the method group.
        session (APISession): The HTTP session object used to send requests.
        tokens (dict): A dictionary of tokens used for authentication (key: token type, value: token string).
    """

    __slots__ = ("region", "_http", "_tokens")

    def __init__(self, region: str | None, session: APISession, tokens: dict[TokenType, str]):
        self._http = session
        self._tokens = tokens
        self.region = region

    @staticmethod
    def wrap_data(data: dict | list[dict], model: APIObject) -> APIObject:
        """Wraps the provided data into an instance (or instances) of the given model.

        Args:
            data (dict | list[dict]): The data to wrap, either a single dictionary
                or a list of dictionaries.
            model (APIObject): The model class to wrap the data into.

        Returns:
            APIObject: A wrapped model instance or a list of wrapped model instances.

        """
        if isinstance(data, list):
            return [model(**item) for item in data]
        return model(**data)

    @classmethod
    def _required_token(cls, token_type: TokenType) -> callable:
        """A decorator to ensure that the required token is provided before executing the method.

        Args:
            token_type (TokenType): The type of token required for the method.

        Returns:
            callable: The decorated function that ensures a valid token is available.
        """

        def decorator(func) -> callable:
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
        """Returns the name of the group, derived from the class name.

        Returns:
            str: The name of the method group.
        """
        print(type(self).__name__)
        return type(self).__name__.replace("Methods", "").lower()


class RegionsMethods(MethodsGroup):
    def get_all(self, **kwargs) -> list[Region]:
        """Retrieves all regions from the API.

        Args:
            **kwargs: Additional arguments that can be passed to modify the request.

        Returns:
            list[Region]: A list of `Region` objects representing all the regions returned by the API.
        """
        resource = f"/{self.group_name}"
        response = self._http.get(url=resource, params=kwargs)
        return response


class EmissionsMethods(MethodsGroup):
    @MethodsGroup._required_token(TokenType.APPLICATION)
    def get_info(self, **kwargs) -> Emission:
        """Retrieves emission information for the specified region.

        Args:
            **kwargs: Additional arguments for the request.

        Returns:
            Emission: An instance of the `Emission` model containing the emission data retrieved from the API.

        Raises:
            MissingTokenError: If the required `token` is not provided or is missing from the `_tokens` attribute.
        """
        resource = f"{self.region}/{self.group_name[:-1]}"
        headers = {"Authorization": f"Bearer {kwargs.pop('token')}"}
        response = self._http.get(url=resource, headers=headers)
        return self.wrap_data(response.json(), Emission)


class FriendsMethods(MethodsGroup):
    @MethodsGroup._required_token(TokenType.USER)
    def get_all(self, character_name: str, **kwargs) -> list[str]:
        """Retrieves a list of friends for the specified character in the current region.

        Args:
            character_name (str): The name of the character whose friends list is to be fetched.
            **kwargs: Additional arguments for the request.

        Returns:
            list[str]: A list of strings representing the names of the character's friends.

        Raises:
            MissingTokenError: If the required `token` is not provided or is missing from the `_tokens` attribute.
        """
        resource = f"{self.region}/{self.group_name}/{character_name}"
        headers = {"Authorization": f"Bearer {kwargs.pop('token')}"}
        response = self._http.get(url=resource, headers=headers)
        return response.json()


class AuctionMethods(MethodsGroup):
    @MethodsGroup._required_token(TokenType.APPLICATION)
    def get_item_history(self, item_id: str, **kwargs) -> list[AuctionRedeemedLot]:
        """Retrieves the history of a specific item in the auction.

        Args:
            item_id (str): The unique identifier of the item for which to fetch the history.
            **kwargs: Additional query parameters (e.g., date filters, pagination) to refine the request.

        Returns:
            list[AuctionRedeemedLot]: A list of `AuctionRedeemedLot` objects representing the item's price history.

        Raises:
            MissingTokenError: If the required `token` is not provided or is missing from the `_tokens` attribute.
        """
        resource = f"{self.region}/{self.group_name}/{item_id}/history"
        headers = {"Authorization": f"Bearer {kwargs.pop('token')}"}
        response = self._http.get(url=resource, headers=headers, params=kwargs)
        return self.wrap_data(response.json()["prices"], AuctionRedeemedLot)

    @MethodsGroup._required_token(TokenType.APPLICATION)
    def get_item_lots(self, item_id: str, **kwargs) -> list[AuctionLot]:
        """Retrieves the auction lots for a specific item.

        Args:
            item_id (str): The unique identifier of the item for which to fetch the auction lots.
            **kwargs: Additional query parameters (e.g., filters, pagination) to refine the request.

        Returns:
            list[AuctionLot]: A list of `AuctionLot` objects representing the auction lots the item has been listed in.

        Raises:
            MissingTokenError: If the required `token` is not provided or is missing from the `_tokens` attribute.
        """
        resource = f"{self.region}/{self.group_name}/{item_id}/lots"
        headers = {"Authorization": f"Bearer {kwargs.pop('token')}"}
        response = self._http.get(url=resource, headers=headers, params=kwargs)
        return self.wrap_data(response.json()["lots"], AuctionLot)


class CharactersMethods(MethodsGroup):
    @MethodsGroup._required_token(TokenType.USER)
    def get_all(self, **kwargs) -> list[CharacterInfo]:
        """Retrieves a list of characters in the current region.

        Args:
            **kwargs: Additional query parameters (e.g., filters, pagination) to refine the request.

        Returns:
            list[CharacterInfo]: A list of `CharacterInfo` objects containing information about the characters.

        Raises:
            MissingTokenError: If the required `token` is not provided or is missing from the `_tokens` attribute.
        """
        resource = f"{self.region}/{self.group_name}"
        headers = {"Authorization": f"Bearer {kwargs.pop('token')}"}
        response = self._http.get(url=resource, headers=headers, params=kwargs)
        return self.wrap_data(response.json(), CharacterInfo)

    @MethodsGroup._required_token(TokenType.APPLICATION)
    def get_profile(self, character_name: str, **kwargs) -> FullCharacterInfo:
        """Retrieves the full profile of a specific character by name.

        Args:
            character_name (str): The name of the character whose profile is to be fetched.
            **kwargs: Additional query parameters (e.g., filters, pagination) to refine the request.

        Returns:
            FullCharacterInfo: A `FullCharacterInfo` object containing the full profile of the specified character.

        Raises:
            MissingTokenError: If the required `token` is not provided or is missing from the `_tokens` attribute.
        """
        resource = f"{self.region}/{self.group_name[:-1]}/by-name/{character_name}/profile"
        headers = {"Authorization": f"Bearer {kwargs.pop('token')}"}
        response = self._http.get(url=resource, headers=headers, params=kwargs)
        return self.wrap_data(response.json(), FullCharacterInfo)


class ClansMethods(MethodsGroup):
    @MethodsGroup._required_token(TokenType.APPLICATION)
    def get_info(self, clan_id: str, **kwargs) -> Clan:
        """Retrieves information about a specific clan by its ID.

        Args:
            clan_id (str): The unique identifier of the clan whose information is to be fetched.
            **kwargs: Additional query parameters (e.g., filters) to refine the request.

        Returns:
            Clan: A `Clan` object containing detailed information about the specified clan.

        Raises:
            MissingTokenError: If the required `token` is not provided or is missing from the `_tokens` attribute.
        """
        resource = f"{self.region}/{self.group_name[:-1]}/{clan_id}/info"
        headers = {"Authorization": f"Bearer {kwargs.pop('token')}"}
        response = self._http.get(url=resource, headers=headers, params=kwargs)
        return self.wrap_data(response.json(), Clan)

    @MethodsGroup._required_token(TokenType.USER)
    def get_members(self, clan_id: str, **kwargs) -> list[ClanMember]:
        """Retrieves a list of members in a specific clan by its ID.

        Args:
            clan_id (str): The unique identifier of the clan whose members are to be fetched.
            **kwargs: Additional query parameters (e.g., pagination) to refine the request.

        Returns:
            list[ClanMember]: A list of `ClanMember` objects representing the members of the specified clan.

        Raises:
            MissingTokenError: If the required `token` is not provided or is missing from the `_tokens` attribute.
        """
        resource = f"{self.region}/{self.group_name[:-1]}/{clan_id}/members"
        headers = {"Authorization": f"Bearer {kwargs.pop('token')}"}
        response = self._http.get(url=resource, headers=headers, params=kwargs)
        return self.wrap_data(response.json(), ClanMember)

    @MethodsGroup._required_token(TokenType.APPLICATION)
    def get_all(self, **kwargs) -> list[Clan]:
        """Retrieves a list of all clans in the current region.


        Args:
            **kwargs: Additional query parameters (e.g., filters, pagination) to refine the request.

        Returns:
            list[Clan]: A list of `Clan` objects representing all the clans in the region.

        Raises:
            MissingTokenError: If the required `token` is not provided or is missing from the `_tokens` attribute.
        """
        resource = f"{self.region}/{self.group_name}"
        headers = {"Authorization": f"Bearer {kwargs.pop('token')}"}
        response = self._http.get(url=resource, headers=headers, params=kwargs)
        return self.wrap_data(response.json()["data"], Clan)


class MethodsGroupFabric:
    """A factory class responsible for creating method groups for different API endpoints.

    The MethodsGroupFabric class provides an interface to create instances of different
    method groups based on the specified group type (e.g., "regions", "emissions", etc.).
    Each method group can be used to interact with a particular set of API endpoints.

    Attributes:
        _method_groups (dict): A mapping of method group names to corresponding class types.
        _group_class (type): The class type associated with the given method group.
        _tokens (dict): A dictionary containing tokens used for authorization.
        _http (APISession): An HTTP session object used to make requests.

    Args:
        group (str): The name of the method group. Must be one of the predefined groups in `_method_groups`.
        http (APISession): The HTTP session used to send requests.
        tokens (dict): A dictionary of tokens used for authentication (key: token type, value: token string).

    Raises:
        InvalidMethodGroup: If the provided `group` is not a valid method group name.
    """

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
