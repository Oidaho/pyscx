import png  # type: ignore[import-untyped]

from pyscx.models import StalcraftEntity, StalcraftIcon

from ._abc import Deserializer
from ._types import ReadBuffer


class PngDeserializer(Deserializer[StalcraftIcon]):
    """Deserializer for parsing png image data from buffers."""

    _extension = ".png"
    target_type = StalcraftIcon

    def deserialize(self, buffer: ReadBuffer) -> StalcraftIcon:
        """Deserialize image data from a buffer.

        Args:
            buffer (ReadBuffer): File-like binary buffer containing the image data.

        Returns:
            StalcraftIcon: Instance of StalcraftIcon representing the deserialized image.
        """
        reader = png.Reader(bytes=buffer.read())

        width, height, rows, metadata = reader.read()

        channels = metadata.get("planes", 3)
        pixels = b"".join(bytes(row) for row in rows)

        return self.target_type(width=width, height=height, pixels=pixels, channels=channels)


class JsonDeserializer[T: StalcraftEntity](Deserializer[T]):
    """Deserializer for parsing entity data from buffers."""

    _extension = ".json"

    def __init__(self, target_type: type[T]) -> None:
        """Class initialization.

        Args:
            target_type (type[T]): Specific StalcraftEntity subclass that this
                deserializer will produce.
        """
        self.target_type = target_type

    def deserialize(self, buffer: ReadBuffer) -> T:
        """Deserialize JSON data from a buffer.

        Args:
            buffer (ReadBuffer): File-like binary buffer containing the JSON data.

        Returns:
            T: Instance of the specified StalcraftEntity subclass
                representing the deserialized entity.
        """
        json_str = buffer.read().decode("utf-8")
        return self.target_type.model_validate_json(json_str)
