from datetime import datetime
from enum import StrEnum
from typing import Annotated

from pydantic import Field

from ._base import StalcraftEntity


class ClanMemberRank(StrEnum):
    """A list of ranks within a unit (clan)."""

    RECRUIT = "RECRUIT"
    COMMONER = "COMMONER"
    SOLDIER = "SOLIDER"  # API spelling error
    SERGEANT = "SERGANT"  # API spelling error
    OFFICER = "OFFICER"
    COLONEL = "COLONEL"
    LEADER = "LEADER"


class Clan(StalcraftEntity):
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


class ClanMember(StalcraftEntity):
    """Representation of data about a member of a unit (clan).

    Attributes:
        name (str): The in-game name of the member.
        rank (ClanMemberRank): The rank of the member within the unit, which is defined by the `ClanMemberRank` enum.
        join_time (datetime): The moment when the member joined the unit. This is the date and time of their joining.
    """

    name: Annotated[str, Field(alias="name")]
    rank: Annotated[ClanMemberRank, Field(alias="rank")]
    join_time: Annotated[datetime, Field(alias="joinTime")]
