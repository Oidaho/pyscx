from pathlib import Path

from pyscx.database import ReadingBackend

# TODO: Consider using the GitHub API in addition to the RawContent API
# for example, to obtain file data (list of files in a directory, metadata, etc.).


class Node:
    """A node for building API request trees."""

    __slots__ = ("_backend", "_uri", "_ext")

    def __init__(
        self, backend: ReadingBackend, uri: Path | None = None, extension: str = ".json"
    ) -> None:
        """Class initialization.

        Args:
            backend (ReadingBackend): Backend responsible for reading data from the source.
            uri (Path | None): URI to the file source. Defaults to None.
            extension (str): File extension for data files. Defaults to ".json".
        """
        self._backend = backend
        self._uri = uri or Path("/")
        self._ext = extension

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
        return class_(self._backend, self._uri / resource, extension or self._ext)


class GetterNode(Node):
    """Node that fetches data by ID using the backend."""

    async def __call__(self, id: str) -> None:
        """Fetch data by ID using the backend.

        Args:
            id (str): _description_
        """
        uri = self._uri / (id + self._ext)

        await self._backend.read(uri)


class VariantsGetterNode(GetterNode):
    """Node that fetches data variants by ID and number using the backend.

    Inherits from GetterNode to reuse the ID fetching logic and adds functionality
    for handling variants.
    """

    async def variants(self, id: str, number: int) -> None:
        """Fetch data variants by ID and number using the backend.

        Args:
            id (str): ID of the data to fetch (filename exactly).
            number (int): Number of the variant to fetch.
        """
        file_name = str(number) + self._ext
        uri = self._uri.joinpath(*["_variants", id], file_name)

        await self._backend.read(uri)
