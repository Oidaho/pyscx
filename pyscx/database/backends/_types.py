from collections.abc import AsyncIterator
from typing import Protocol, AsyncContextManager


class ReadBuffer(Protocol):
    """Minimal file-like binary buffer protocol."""

    def read(self, size: int = -1) -> bytes: ...
    def seek(self, offset: int, whence: int = 0) -> int: ...
    def tell(self) -> int: ...
    def close(self) -> None: ...


class StreamBuffer(AsyncIterator[bytes], AsyncContextManager, Protocol):
    """Async streaming file-like buffer protocol."""

    async def __anext__(self) -> bytes: ...  # Specify return value
    async def close(self) -> None: ...
