from collections.abc import AsyncIterator
from pathlib import Path
from typing import Self

import aiofiles
import aiohttp

from ._types import StreamBuffer


class LocalStreamBuffer(StreamBuffer):
    """Async streaming file-like buffer for local repository."""

    def __init__(self, path: Path, chunk_size: int = 65536):
        """Class initialization.

        Args:
            path (Path): Path to the repository root.
            chunk_size (int, optional): Size of each chunk to read.
                Defaults to 65536.
        """
        self._path = path
        self._chunk_size = chunk_size

    def __aiter__(self) -> AsyncIterator[bytes]:
        """Return an asynchronous iterator over the file chunks."""
        return self

    async def __aenter__(self) -> Self:
        """Open the file asynchronously and prepare for iteration."""
        self._file = await aiofiles.open(self._path, "rb")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Close the file asynchronously when exiting the context."""
        await self.close()

    async def __anext__(self) -> bytes:
        """Read chunks of the file asynchronously and return them until EOF is reached."""
        chunk = await self._file.read(self._chunk_size)
        if not chunk:
            raise StopAsyncIteration

        return chunk

    async def close(self) -> None:
        """Close the file asynchronously."""
        if self._file:
            await self._file.close()


class RemoteStreamBuffer(StreamBuffer):
    """Async streaming file-like buffer for remote repository."""

    def __init__(self, session: aiohttp.ClientSession, url: str, chunk_size: int = 65536):
        """Class initialization.

        Args:
            session (aiohttp.ClientSession): Aiohttp client session.
            url (str): URL of the remote resource (e.g., a file).
            chunk_size (int, optional): Size of each chunk to read. Defaults to 65536.
        """
        self._session = session
        self._url = url
        self._chunk_size = chunk_size

    async def __aenter__(self) -> Self:
        """Open the URL asynchronously and prepare for iteration."""
        self._resp = await self._session.get(self._url)
        self._resp.raise_for_status()

        self._aiter = self._resp.content.iter_chunked(self._chunk_size)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close the response asynchronously when exiting the context."""
        await self.close()

    def __aiter__(self):
        """Return an asynchronous iterator over the response content chunks."""
        return self

    async def __anext__(self) -> bytes:
        """Proxy next chunk from the response content iterator."""
        return await self._aiter.__anext__()

    async def close(self) -> None:
        """Close response asynchronously."""
        if self._resp:
            self._resp.close()
