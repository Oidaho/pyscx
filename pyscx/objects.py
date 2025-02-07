from pydantic import Annotated, BaseModel, Field, datetime
from enum import Enum


class APIObject(BaseModel):
    def raw(self) -> dict[str, any]:
        return self.model_dump(by_alias=True)


# ! REGION SCHEMAS
# ! ==============
class Region(APIObject):
    id: Annotated[str, Field(alias="id")]
    name: Annotated[str, Field(alias="name")]


# ! EMISSION SCHEMAS
# ! ================
class Emission(APIObject):
    current_start: Annotated[datetime, Field(alias="currentStart")]
    previous_start: Annotated[datetime, Field(alias="previousStart")]
    previous_end: Annotated[datetime, Field(alias="previousEnd")]


# ! AUCTION SCHEMAS
# ! ===============
class AuctionLot(APIObject):
    item_id: Annotated[str, Field(alias="itemId")]
    amount: Annotated[int, Field(alias="amount")]
    start_price: Annotated[int, Field(alias="startPrice")]
    current_price: Annotated[int, Field(alias="currentPrice")]
    buyout_price: Annotated[int, Field(alias="buyoutPrice")]
    start_time: Annotated[datetime, Field(alias="startTime")]
    end_time: Annotated[datetime, Field(alias="endTime")]
    additional: Annotated[dict[str, any], Field(alias="dict")]


class AuctionRedeemedLot(APIObject):
    amount: Annotated[int, Field(alias="amount")]
    price: Annotated[int, Field(alias="price")]
    time: Annotated[datetime, Field(alias="time")]
    additional: Annotated[dict[str, any], Field(alias="dict")]


# ! CLAN SCHEMAS
# ! ============
class Clan(APIObject):
    id: Annotated[str, Field(alias="id")]
    name: Annotated[str, Field(alias="name")]
    tag: Annotated[str, Field(alias="tag")]
    level: Annotated[int, Field(alias="level")]
    level_points: Annotated[int, Field(alias="levelPoints")]
    registration_time: Annotated[datetime, Field(alias="registrationTime")]
    alliance: Annotated[str, Field(alias="alliance")]
    description: Annotated[str, Field(alias="description")]
    leader: Annotated[str, Field(alias="leader")]
    member_count: Annotated[str, Field(alias="memberCount")]


class ClanMemberRank(Enum):
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
    name: Annotated[str, Field(alias="name")]
    rank: Annotated[ClanMemberRank, Field(alias="rank")]
    join_time: Annotated[datetime, Field(alias="joinTime")]


# ! CHARACTER SCHEMAS
# ! =================
class CharacterStatType(Enum):
    INTEGER = "INTEGER"
    DECIMAL = "DECIMAL"
    DATE = "DATE"
    DURATION = "DURATION"


class CharacterStat(APIObject):
    id: Annotated[str, Field(alias="id")]
    type: Annotated[CharacterStatType, Field(alias="type")]
    value: Annotated[dict[str, any], Field(alias="dict")]


class CharacterMeta(APIObject):
    id: Annotated[str, Field(alias="id")]
    name: Annotated[str, Field(alias="name")]
    creation_time: Annotated[datetime, Field(alias="creationTime")]


class CharacterClan(APIObject):
    info: Annotated[Clan, Field(alias="info")]
    member: Annotated[ClanMember, Field(alias="member")]


class CharacterInfo(APIObject):
    information: Annotated[CharacterMeta, Field(alias="information")]
    clan: Annotated[CharacterClan, Field(alias="clan")]


class FullCharacterInfo(APIObject):
    uuid: Annotated[str, Field(alias="uuid")]
    name: Annotated[str, Field(alias="username")]
    status: Annotated[str, Field(alias="status")]
    alliance: Annotated[str, Field(alias="alliance")]
    last_login: Annotated[datetime, Field(alias="lastLogin")]
    displayed_achievements: Annotated[list[str], Field(alias="displayedAchievements")]

    clan: Annotated[CharacterClan, Field(alias="clan")]
    stat: Annotated[list[CharacterStat], Field(alias="stat")]
