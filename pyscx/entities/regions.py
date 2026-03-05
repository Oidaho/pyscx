from typing import Annotated

from pydantic import Field

from ._base import StalcraftEntity


class Region(StalcraftEntity):
    """Representation of data about the region where the game servers are located.

    Attributes:
        id (str): A unique identifier for the region.
        name (str): The name of the region.
    """

    id: Annotated[str, Field(alias="id")]
    name: Annotated[str, Field(alias="name")]
