from PIL.Image import Image
from PIL.Image import open as pil_open
from io import BytesIO
from pyscx.entities import StalcraftEntity

from ._abc import Deserializer
from ._types import ReadBuffer


class PngDeserializer(Deserializer[Image]):
    """Deserializer for parsing png image data from buffers."""

    _extension = ".png"
    target_type = Image  # * Image type can be instanced only with PIL.Image.open

    async def deserialize(self, buffer: ReadBuffer) -> Image:
        """Deserialize image data from a buffer.

        Args:
            buffer (ReadBuffer): File-like binary buffer containing the image data.

        Returns:
            Image: An instance of PIL.Image (still unloaded) representing the deserialized image.
        """
        # PIL.Image.open can handle both ReadBuffer and StreamBuffer as they both
        # implement the necessary file-like interface.

        return pil_open(BytesIO(buffer.read()))


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

    async def deserialize(self, buffer: ReadBuffer) -> T:
        """Deserialize JSON data from a buffer.

        Args:
            buffer (ReadBuffer): File-like binary buffer containing the JSON data.

        Returns:
            T: Instance of the specified StalcraftEntity subclass
                representing the deserialized entity.
        """
        json_str = buffer.read().decode("utf-8")
        return self.target_type.model_validate_json(json_str)
