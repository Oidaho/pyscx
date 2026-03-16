from datetime import datetime
from typing import Annotated, Any

from pydantic import Field

from ._base import StalcraftEntity


class AuctionLot(StalcraftEntity):
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


class RedeemedAuctionLot(StalcraftEntity):
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
