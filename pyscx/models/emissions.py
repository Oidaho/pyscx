from datetime import datetime
from typing import Annotated

from pydantic import Field

from ._base import StalcraftEntity


# {
#     "currentStart": "2019-08-24T14:15:22Z",
#     "previousStart": "2019-08-24T14:15:22Z",
#     "previousEnd": "2019-08-24T14:15:22Z",
# }


class Emission(StalcraftEntity):
    """_summary_"""

    current_start: Annotated[datetime, Field(alias="currentStart")]
    previous_start: Annotated[datetime, Field(alias="previousStart")]
    previous_end: Annotated[datetime, Field(alias="previousEnd")]
