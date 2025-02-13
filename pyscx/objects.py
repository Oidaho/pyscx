from datetime import datetime
from enum import Enum
from typing import Annotated, Any

from pydantic import BaseModel, Field


class APIObject(BaseModel):
    """An API object that provides data in a convenient form.

    This class extends from Pydantic's `BaseModel` and is designed to represent API responses in a
    structured and convenient format. When data is returned from the STALCRAFT: X API, the data is
    automatically wrapped in this class for easy access.

    The class supports Pydantic's data validation and serialization, making it easier to handle API
    responses and convert them into Python objects.
    """

    def raw(self) -> dict[str, Any]:
        """Raw representation of the object as it was obtained from the STALCRAFT: X API.

        Returns:
            dict[str, Any]: A dictionary containing the raw data of the object as it was received from the API.
        """
        return self.model_dump(by_alias=True, mode="json", exclude_none=True)


class Region(APIObject):
    """Representation of data about the region where the game servers are located.

    Attributes:
        id (str): A unique identifier for the region.
        name (str): The name of the region.
    """

    id: Annotated[str, Field(alias="id")]
    name: Annotated[str, Field(alias="name")]


class Emission(APIObject):
    """Representation of emissions data in the game.

    Attributes:
        current_start (datetime): The moment when the current emission iteration began.
        previous_start (datetime): The moment when the previous emission iteration began.
        previous_end (datetime): The moment when the previous emission iteration ended.
    """

    current_start: Annotated[datetime, Field(alias="currentStart")]
    previous_start: Annotated[datetime, Field(alias="previousStart")]
    previous_end: Annotated[datetime, Field(alias="previousEnd")]


class AuctionLot(APIObject):
    """Representation of an active auction lot for an item.

    Attributes:
        item_id (str): Unique identifier of the in-game item.
        amount (int): Number of items in the lot.
        start_price (int): Starting price of the auction lot.
        current_price (int, optional): Current bid price for the auction lot. Defaults to None.
        buyout_price (int): Buyout price of the auction lot.
        start_time (datetime): Datetime when the auction lot was created.
        end_time (datetime): Datetime when the auction lot will close.
        additional (dict[str, Any]): Additional data about the lot, such as specific conditions or properties.
    """

    item_id: Annotated[str, Field(alias="itemId")]
    amount: Annotated[int, Field(alias="amount")]
    start_price: Annotated[int, Field(alias="startPrice")]
    current_price: Annotated[int | None, Field(alias="currentPrice", default=None)]
    buyout_price: Annotated[int, Field(alias="buyoutPrice")]
    start_time: Annotated[datetime, Field(alias="startTime")]
    end_time: Annotated[datetime, Field(alias="endTime")]
    additional: Annotated[dict[str, Any], Field(alias="additional")]


class AuctionRedeemedLot(APIObject):
    """Representation of a purchased auction lot for an item.

    Attributes:
        amount (int): Number of items in the lot.
        price (int): Final sale price of the lot.
        time (datetime): Datetime when the lot was sold.
        additional (dict[str, Any]): Additional data about the lot, such as special conditions or properties.
    """

    amount: Annotated[int, Field(alias="amount")]
    price: Annotated[int, Field(alias="price")]
    time: Annotated[datetime, Field(alias="time")]
    additional: Annotated[dict[str, Any], Field(alias="additional")]


class Clan(APIObject):
    """Representation of in-game unit (clan) data.

    Attributes:
        id (str): Unique unit identifier.
        name (str): Unit name.
        tag (str): Unit tag.
        level (int): Current unit level.
        level_points (int): Number of unit level points.
        registration_time (datetime): Datetime when the unit was created.
        alliance (str): Grouping to which the unit belongs.
        description (str): Public unit description.
        leader (str): In-game name of the unit leader.
        member_count (int): Number of active members in the unit.
    """

    id: Annotated[str, Field(alias="id")]
    name: Annotated[str, Field(alias="name")]
    tag: Annotated[str, Field(alias="tag")]
    level: Annotated[int, Field(alias="level")]
    level_points: Annotated[int, Field(alias="levelPoints")]
    registration_time: Annotated[datetime, Field(alias="registrationTime")]
    alliance: Annotated[str, Field(alias="alliance")]
    description: Annotated[str, Field(alias="description")]
    leader: Annotated[str, Field(alias="leader")]
    member_count: Annotated[int, Field(alias="memberCount")]


class ClanMemberRank(Enum):
    """A list of ranks within a unit (clan)."""

    RECRUIT = "RECRUIT"
    COMMONER = "COMMONER"
    # API spelling error
    SOLDIER = "SOLIDER"
    SERGEANT = "SERGANT"
    # -----------------
    OFFICER = "OFFICER"
    COLONEL = "COLONEL"
    LEADER = "LEADER"


class ClanMember(APIObject):
    """Representation of data about a member of a unit (clan).

    Attributes:
        name (str): The in-game name of the member.
        rank (ClanMemberRank): The rank of the member within the unit, which is defined by the `ClanMemberRank` enum.
        join_time (datetime): The moment when the member joined the unit. This is the date and time of their joining.
    """

    name: Annotated[str, Field(alias="name")]
    rank: Annotated[ClanMemberRank, Field(alias="rank")]
    join_time: Annotated[datetime, Field(alias="joinTime")]


class CharacterStatType(Enum):
    """A list of supported types for player statistic values."""

    INTEGER = "INTEGER"
    DECIMAL = "DECIMAL"
    DATE = "DATE"
    DURATION = "DURATION"


class CharacterStat(APIObject):
    """Representation of data for a specific player statistic.

    Attributes:
        id (str): The unique identifier of the statistic. This could be the name or key of the statistic.
        type (CharacterStatType): The type of the statistic value, which is defined by the `CharacterStatType` enum.
        value (dict[str, Any]): A dictionary that contains the actual values of the statistic.
    """

    id: Annotated[str, Field(alias="id")]
    type: Annotated[CharacterStatType, Field(alias="type")]
    value: Annotated[dict[str, Any], Field(alias="value")]


class CharacterMeta(APIObject):
    """Representation of the primary data about a character.

    Attributes:
        id (str): The unique identifier of the character.
        name (str): The in-game name of the character.
        creation_time (datetime): The moment when the character was created.
    """

    id: Annotated[str, Field(alias="id")]
    name: Annotated[str, Field(alias="name")]
    creation_time: Annotated[datetime, Field(alias="creationTime")]


class CharacterClan(APIObject):
    """Representation of the primary data about a character.

    Attributes:
        id (str): The unique identifier of the character.
        name (str): The in-game name of the character.
        creation_time (datetime): The moment when the character was created.
    """

    info: Annotated[Clan, Field(alias="info")]
    member: Annotated[ClanMember, Field(alias="member")]


class CharacterInfo(APIObject):
    """Representation of data about a game character.

    Attributes:
        information (CharacterMeta): Primary information about the character, including
            the character's unique ID, name, and creation time.
        clan (CharacterClan): Information about the character's unit (clan), if the character
            is part of one. This includes details such as the clan's name and rank.
    """

    information: Annotated[CharacterMeta, Field(alias="information")]
    clan: Annotated[CharacterClan, Field(alias="clan")]


class FullCharacterInfo(APIObject):
    """Representation of complete information about a game character.

    Attributes:
        uuid (str): The unique universal identifier of the game character.
        name (str): The name of the game character as it appears in the game.
        status (str): The online status of the game character (e.g., "online", "offline").
        alliance (str): The grouping or faction to which the game character belongs.
        last_login (datetime): The last time the character logged into the game.
        displayed_achievements (list[str]): A list of identifiers for the achievements or statistics
            pinned to the character's profile.
        clan (CharacterClan): Information about the character's unit (clan). This includes details
            such as the clan's name, rank, and other related information.
        stats (list[CharacterStat]): A list of representations of the character's statistics.
            Each statistic includes an ID, value, and other associated metadata.
    """

    uuid: Annotated[str, Field(alias="uuid")]
    name: Annotated[str, Field(alias="username")]
    status: Annotated[str, Field(alias="status")]
    alliance: Annotated[str, Field(alias="alliance")]
    last_login: Annotated[datetime, Field(alias="lastLogin")]
    displayed_achievements: Annotated[list[str], Field(alias="displayedAchievements")]

    clan: Annotated[CharacterClan, Field(alias="clan")]
    stats: Annotated[list[CharacterStat], Field(alias="stats")]
