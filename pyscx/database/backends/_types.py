from collections.abc import AsyncIterator
from typing import Protocol, AsyncContextManager


class ReadBuffer(Protocol):
    """Minimal file-like binary buffer protocol."""

    def read(self, size: int = -1) -> bytes:
        """Read at most size bytes, returned as a bytes object.

        If the size argument is negative, read until EOF is reached.
        Return an empty bytes object at EOF.
        """

    def seek(self, offset: int, whence: int = 0) -> int:
        """Change stream position.

        Seek to byte offset pos relative to position indicated by whence:
            0  Start of stream (the default).  pos should be >= 0;
            1  Current position - pos may be negative;
            2  End of stream - pos usually negative.

        Returns the new absolute position.
        """

    def tell(self) -> int:
        """Current file position, an integer"""

    def close(self) -> None:
        """Disable all I/O operations."""


class StreamBuffer(AsyncIterator[bytes], AsyncContextManager, Protocol):
    """Async streaming file-like buffer protocol."""

    async def __anext__(self) -> bytes: ...  # Specify return value
    async def close(self) -> None:
        """Disable all I/O operations."""
