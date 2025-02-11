from datetime import datetime
from enum import Enum
from typing import Annotated, Any

from pydantic import BaseModel, Field


class APIObject(BaseModel):
    """An API object that provides data in a convenient form.

    It is a Pydantic model, which allows API objects to automatically wrap
    the data received in response to a request to the STALCRAFT: X API.
    """

    def raw(self) -> dict[str, Any]:
        """Raw representation of the object as it was obtained from the STALCRAFT: X API."""
        return self.model_dump(by_alias=True, mode="json", exclude_none=True)


# ! REGION SCHEMAS
# ! ==============
class Region(APIObject):
    """Representation of data about the region where the game servers are located.

    Attributes:
        id (str): A unique identifier for the region.
        name (str): The name of the region.
    """

    id: Annotated[str, Field(alias="id")]
    name: Annotated[str, Field(alias="name")]


# ! EMISSION SCHEMAS
# ! ================
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


# ! AUCTION SCHEMAS
# ! ===============
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
        additional (dict[str, Any]): Additional data about the lot.
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
        additional (dict[str, Any]): Additional data about the lot.
    """

    amount: Annotated[int, Field(alias="amount")]
    price: Annotated[int, Field(alias="price")]
    time: Annotated[datetime, Field(alias="time")]
    additional: Annotated[dict[str, Any], Field(alias="additional")]


# ! CLAN SCHEMAS
# ! ============
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
        rank (ClanMemberRank): The rank of the member within the unit.
        join_time (datetime): The moment when the member joined the unit.
    """

    name: Annotated[str, Field(alias="name")]
    rank: Annotated[ClanMemberRank, Field(alias="rank")]
    join_time: Annotated[datetime, Field(alias="joinTime")]


# ! CHARACTER SCHEMAS
# ! =================
class CharacterStatType(Enum):
    """A list of supported types for player statistic values."""

    INTEGER = "INTEGER"
    DECIMAL = "DECIMAL"
    DATE = "DATE"
    DURATION = "DURATION"


class CharacterStat(APIObject):
    """Representation of data for a specific player statistic.

    Attributes:
        id (str): The unique identifier of the statistic.
        type (CharacterStatType): The type of the statistic value.
        value (dict[str, Any]): A dictionary of statistic values.
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
    """Representation of data about the unit (clan) where the character is a member.

    Attributes:
        info (Clan): Information about the unit (clan).
        member (str): Information about the character as a member of the unit (clan).
    """

    info: Annotated[Clan, Field(alias="info")]
    member: Annotated[ClanMember, Field(alias="member")]


class CharacterInfo(APIObject):
    """Representation of data about a game character.

    Attributes:
        information (CharacterMeta): Primary information about the character.
        clan (CharacterClan): Information about the unit (clan).
    """

    information: Annotated[CharacterMeta, Field(alias="information")]
    clan: Annotated[CharacterClan, Field(alias="clan")]


class FullCharacterInfo(APIObject):
    """Representation of complete information about a game character.

    Attributes:
        uuid (str): The unique universal identifier of the game character.
        name (str): The name of the game character.
        status (str): The online status of the game character.
        alliance (str): The grouping in which the game character is affiliated.
        last_login (datetime): The last time the character logged into the game.
        displayed_achievements (list[str]): A list of identifiers for statistics pinned to the profile.
        clan (CharacterClan): Information about the unit (clan).
        stat (list[CharacterStat]): A list of representations of the character's statistics.
    """

    uuid: Annotated[str, Field(alias="uuid")]
    name: Annotated[str, Field(alias="username")]
    status: Annotated[str, Field(alias="status")]
    alliance: Annotated[str, Field(alias="alliance")]
    last_login: Annotated[datetime, Field(alias="lastLogin")]
    displayed_achievements: Annotated[list[str], Field(alias="displayedAchievements")]

    clan: Annotated[CharacterClan, Field(alias="clan")]
    stats: Annotated[list[CharacterStat], Field(alias="stats")]
