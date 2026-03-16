from abc import ABC, abstractmethod
from pathlib import Path

from pyscx.models import StalcraftEntity, StalcraftIcon

from ._types import ReadBuffer, StreamBuffer


class ReadingBackend(ABC):
    """Abstract backend for reading files."""

    @abstractmethod
    async def read(self, uri: str | Path) -> ReadBuffer:
        """Read full file into memory.

        Args:
            uri (str | Path): URI to the target file.

        Raises:
            NotImplementedError: Method is not implemented in the child class.

        Returns:
            ReadBuffer: File-like binary buffer.
        """
        msg = "Method is not implemented in the child class."
        raise NotImplementedError(msg) from None

    @abstractmethod
    def stream(self, uri: str | Path, chunk_size: int = 65536) -> StreamBuffer:
        """Return a streamable buffer (used in async with).

        Args:
            uri (str | Path):  URI to the target file.
            chunk_size (int, optional): Streaming chunk size. Defaults to 65536.

        Raises:
            NotImplementedError: Method is not implemented in the child class.

        Returns:
            StreamBuffer: Streaming file-like binary buffer.
        """

        msg = "The method is not implemented in the child class."

        raise NotImplementedError(msg) from None


class Deserializer[T: StalcraftEntity | StalcraftIcon](ABC):
    """Abstract deserializer for parsing data from buffers."""

    _extension: str
    target_type: type[T]

    @abstractmethod
    async def deserialize(self, buffer: ReadBuffer) -> T:
        """Deserialize data from a buffer.

        Args:
            buffer (ReadBuffer): File-like binary buffer containing the
                data to deserialize.
        """
        msg = "The method is not implemented in the child class."
        raise NotImplementedError(msg) from None

    @property
    def ext(self) -> str:
        """File extension associated with this deserializer."""
        return self._extension

    @ext.setter
    def ext(self, value: str) -> None:
        """File extension setter for the deserializer."""
        self._extension = value
