from datetime import datetime
from typing import Annotated

from pydantic import Field

from ._base import StalcraftEntity


class Emission(StalcraftEntity):
    """Representation of emissions data in the game.

    Attributes:
        current_start (datetime): The moment when the current emission iteration began.
        previous_start (datetime): The moment when the previous emission iteration began.
        previous_end (datetime): The moment when the previous emission iteration ended.
    """

    current_start: Annotated[datetime, Field(alias="currentStart")]
    previous_start: Annotated[datetime, Field(alias="previousStart")]
    previous_end: Annotated[datetime, Field(alias="previousEnd")]
