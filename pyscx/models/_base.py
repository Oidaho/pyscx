from typing import Any, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from PIL.Image import Image as PILImage


class StalcraftEntity(BaseModel):
    """An API object that provides data in a convenient form.

    This class extends from Pydantic's `BaseModel` and is designed to represent API responses in a
    structured and convenient format. When data is returned from the STALCRAFT: X API or the
    STALCRAFT: X repository items database, the data is automatically wrapped in this class
    for easy access.

    The class supports Pydantic's data validation and serialization, making it easier to handle API
    responses and convert them into Python objects.
    """

    model_config = ConfigDict(validate_by_alias=True)

    def raw(self) -> dict[str, Any]:
        """Raw representation of the object as it was obtained from the STALCRAFT: X API or the
        STALCRAFT: X repository items database.

        Returns:
            dict[str, Any]: A dictionary containing the raw data of the object as it was received from the API.
        """
        return self.model_dump(by_alias=True, mode="json", exclude_none=True)


class StalcraftIcon(BaseModel):
    """Representation of an icon image for an in-game item."""

    width: int
    height: int
    pixels: bytes
    channels: int = 4
    format: str = "PNG"

    def to_pillow(self) -> PILImage:
        """Convert to PIL.Image (with lazy import).
        Requires Pillow installed only when called.

        Raises:
            RuntimeError: if Pillow is not installed.
            ValueError: if channels is unsupported.

        Returns:
            PILImage: PIL.Image object.
        """
        try:
            from PIL import Image as _PILImage

        except Exception as exc:
            msg = "Pillow is required to convert to PIL.Image; install pillow."
            raise RuntimeError(msg) from exc

        mode_map = {1: "L", 2: "LA", 3: "RGB", 4: "RGBA"}
        mode = mode_map.get(self.channels)
        if mode is None:
            raise ValueError(f"Unsupported channel count: {self.channels}")

        return _PILImage.frombytes(mode, (self.width, self.height), self.pixels)
