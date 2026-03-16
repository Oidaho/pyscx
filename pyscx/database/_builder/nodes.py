from pathlib import Path
from typing import Any

from pyscx.database.backends import Deserializer, ReadBuffer, ReadingBackend

# TODO: Consider using the GitHub API in addition to the RawContent API
# for example, to obtain file data (list of files in a directory, metadata, etc.).


class Node:
    """A node for building API request trees."""

    __slots__ = ("_backend", "_deserializer", "_uri")

    def __init__(
        self, backend: ReadingBackend, deserializer: Deserializer, uri: Path | None = None
    ) -> None:
        """Class initialization.

        Args:
            backend (ReadingBackend): Backend responsible for reading data from the source.
            deserializer (Deserializer): Deserializer for data buffers.
            uri (Path | None): URI to the file source. Defaults to None.
        """
        self._backend = backend
        self._deserializer = deserializer
        self._uri = uri or Path("/")

    def _child[T: Node](self, class_: type[T], resource: str, extension: str | None = None) -> T:
        """Create a child node with the specified class, resource, and optional extension.

        Args:
            class_ (type[T]): Class of the child node to create.
            resource (str): Resource name to append to the URI for the child node.
            extension (str | None): Optional file extension for the child node. If None, it will
                inherit the extension from the parent node. Defaults to None.

        Returns:
            T: Child node instance.
        """
        return class_(self._backend, self._deserializer, self._uri / resource)


class GetterNode(Node):
    """Node that fetches data by ID using the backend."""

    # TODO: Specify the return type of __call__ method
    async def __call__(self, id: str) -> Any:
        """Fetch data by ID using the backend.

        Args:
            id (str): ID of the data to fetch (filename exactly).
        """
        uri = self._uri / (id + self._deserializer.ext)

        read_buffer = await self.get_buffer(uri)

        return await self._deserializer.deserialize(read_buffer)

    async def get_buffer(self, uri: Path) -> ReadBuffer:
        """Get a read buffer (raw data representation) for the specified URI.

        Args:
            uri (Path): URI for which to get the buffer.

        Returns:
            ReadBuffer: The read buffer for the specified URI.
        """
        return await self._backend.read(uri)


class VariantsGetterNode(GetterNode):
    """Node that fetches data variants by ID and number using the backend.

    Inherits from GetterNode to reuse the ID fetching logic and adds functionality
    for handling variants.
    """

    # TODO: Specify the return type of variants method
    async def variants(self, id: str, number: int) -> Any:
        """Fetch data variants by ID and number using the backend.

        Args:
            id (str): ID of the data to fetch (filename exactly).
            number (int): Number of the variant to fetch.
        """
        file_name = str(number) + self._deserializer.ext
        uri = self._uri.joinpath(*["_variants", id], file_name)

        read_buffer = await self.get_buffer(uri)

        return await self._deserializer.deserialize(read_buffer)
