from abc import ABC, abstractmethod
from pathlib import Path

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
