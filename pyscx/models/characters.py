from datetime import datetime
from enum import StrEnum
from typing import Annotated, Any

from pydantic import Field

from ._base import StalcraftEntity
from .clans import ClanMember, Clan


# {
#   "username": "string",
#   "uuid": "string",
#   "status": "string",
#   "alliance": "string",
#   "lastLogin": "2019-08-24T14:15:22Z",
#   "displayedAchievements": [
#     "string"
#   ],
#   "clan": {
#     "info": {
#       "id": "string",
#       "name": "string",
#       "tag": "string",
#       "level": 0,
#       "levelPoints": 0,
#       "registrationTime": "2019-08-24T14:15:22Z",
#       "alliance": "string",
#       "description": "string",
#       "leader": "string",
#       "memberCount": 0
#     },
#     "member": {
#       "name": "string",
#       "rank": "RECRUIT",
#       "joinTime": "2019-08-24T14:15:22Z"
#     }
#   },
#   "stats": [
#     {
#       "id": "string",
#       "type": "INTEGER",
#       "value": {}
#     }
#   ]
# }


class CharacterStatType(StrEnum):
    """A list of supported types for player statistic values."""

    INTEGER = "INTEGER"
    DECIMAL = "DECIMAL"
    DATE = "DATE"
    DURATION = "DURATION"


class Character(StalcraftEntity):
    """Representation of the primary data about a character.

    Attributes:
        id (str): The unique identifier of the character.
        name (str): The in-game name of the character.
        creation_time (datetime): The moment when the character was created.
    """

    id: Annotated[str, Field(alias="id")]
    name: Annotated[str, Field(alias="name")]
    creation_time: Annotated[datetime, Field(alias="creationTime")]


class CharacterStat(StalcraftEntity):
    """Representation of data for a specific player statistic.

    Attributes:
        id (str): The unique identifier of the statistic. This could be the name or key of the statistic.
        type (CharacterStatType): The type of the statistic value, which is defined by the `CharacterStatType` enum.
        value (dict[str, Any]): A dictionary that contains the actual values of the statistic.
    """

    id: Annotated[str, Field(alias="id")]
    type: Annotated[CharacterStatType, Field(alias="type")]
    value: Annotated[dict[str, Any], Field(alias="value")]


class CharacterClan(StalcraftEntity):
    """Representation of the primary data about a character.

    Attributes:
        id (str): The unique identifier of the character.
        name (str): The in-game name of the character.
        creation_time (datetime): The moment when the character was created.
    """

    info: Annotated[Clan, Field(alias="info")]
    member: Annotated[ClanMember, Field(alias="member")]


class CharacterInfo(StalcraftEntity):
    """Representation of data about a game character.

    Attributes:
        information (CharacterMeta): Primary information about the character, including
            the character's unique ID, name, and creation time.
        clan (CharacterClan): Information about the character's unit (clan), if the character
            is part of one. This includes details such as the clan's name and rank.
    """

    information: Annotated[Character, Field(alias="information")]
    clan: Annotated[CharacterClan, Field(alias="clan")]


class FullCharacterInfo(StalcraftEntity):
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
