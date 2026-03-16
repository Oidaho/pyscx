from typing import Annotated

from pydantic import Field

from ._base import StalcraftEntity


# [
#     {"id": "RU", "name": "RUSSIA"},
#     {"id": "EU", "name": "EUROPE"},
#     {"id": "NA", "name": "NORTH AMERICA"},
#     {"id": "SEA", "name": "SOUTHEAST ASIA"},
#     {"id": "NEA", "name": "NORTHEAST ASIA"},
# ]


class Region(StalcraftEntity):
    """_summary_"""

    code: Annotated[str, Field(alias="id")]
    name: Annotated[str, Field(alias="name")]
