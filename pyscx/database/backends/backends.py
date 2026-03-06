from io import BytesIO
from pathlib import Path
from typing import Final

import aiofiles
import aiohttp

from ._abc import ReadBuffer, ReadingBackend, StreamBuffer
from .buffers import LocalStreamBuffer, RemoteStreamBuffer

STALCRAFT_DATABASE_LOCAL: Final[Path] = Path.cwd() / "scx"  # Where the app was launched from
STALCRAFT_DATABASE_REMOTE: Final[str] = (
    "https://raw.githubusercontent.com/EXBO-Studio/stalcraft-database/main"  # Main branch
)

# TODO: Error handling with PyscxError


class LocalReadingBackend(ReadingBackend):
    """Async Backend for reading files from a local repository."""

    def __init__(self, local_path: str | Path | None = None) -> None:
        """Class initialization.

        Args:
            local_path (str | Path | None): The local path to the root of the repository
                containing the STALCRAFT: X database. If you pass None, the default is to
                assume the database root directory is located at `./scx`. Defaults to None.
        """
        self.local_path = Path(local_path or STALCRAFT_DATABASE_LOCAL)

    async def read(self, uri: str | Path) -> ReadBuffer:
        """Read full file into memory.

        Args:
            uri (str | Path): URI to the target file.

        Returns:
            ReadBuffer: File-like binary buffer.
        """
        path = self.local_path / Path(uri)

        async with aiofiles.open(path, "rb") as f:
            data = await f.read()

        return BytesIO(data)

    def stream(self, uri: str | Path, chunk_size: int = 65536) -> StreamBuffer:
        """Return a streamable buffer (used in async with).

        Args:
            uri (str | Path):  URI to the target file.
            chunk_size (int, optional): Streaming chunk size. Defaults to 65536.

        Returns:
            StreamBuffer: Streaming file-like binary buffer.
        """
        path = self.local_path / Path(uri)

        return LocalStreamBuffer(path, chunk_size)


class RemoteReadingBackend(ReadingBackend):
    """Async Backend for reading files from a remote repository."""

    def __init__(self, session: aiohttp.ClientSession, base_url: str | None = None):
        """Class initialization.

        Args:
            session (aiohttp.ClientSession): Aiohttp session client.
            base_url (str | None, optional): The base URL pointing to the
                GtiHub RawContent API for the remote repository containing the
                STALCRAFT: X database. If you pass the value None, then the
                `EXBO-Studio/stalcraft-database` repository will be selected by default.
                Defaults to None.
        """
        self.base_url = (base_url or STALCRAFT_DATABASE_REMOTE).rstrip("/") + "/"
        self._session = session

    async def read(self, uri: str | Path) -> ReadBuffer:
        """Read full file into memory.

        Args:
            uri (str | Path): URI to the target file.

        Returns:
            ReadBuffer: File-like binary buffer.
        """
        url = self.base_url + (uri.as_posix() if isinstance(uri, Path) else uri).lstrip("/")

        async with self._session.get(url) as resp:
            resp.raise_for_status()

            data = await resp.read()

        return BytesIO(data)

    def stream(self, uri: str | Path, chunk_size: int = 65536) -> StreamBuffer:
        """Return a streamable buffer (used in async with).

        Args:
            uri (str | Path):  URI to the target file.
            chunk_size (int, optional): Streaming chunk size. Defaults to 65536.

        Returns:
            StreamBuffer: Streaming file-like binary buffer.
        """
        url = url = self.base_url + (uri.as_posix() if isinstance(uri, Path) else uri).lstrip("/")

        return RemoteStreamBuffer(self._session, url, chunk_size)
