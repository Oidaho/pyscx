from pathlib import Path

from pyscx.database import ReadingBackend, RemoteReadingBackend

from ._builder import Region


class RepositoryDatabase:
    """RepositoryDatabase class is the main entry point for accessing the stalcraft database.
    It provides access to different regions and their respective data.
    (e.g. weapons, armors, etc.)
    """

    def __init__(self, reading_backend: ReadingBackend | None = None) -> None:
        """Class initialization.

        Args:
            reading_backend (ReadingBackend | None): The ReadingBackend instance to use for
            accessing the database files. If None, a preconfigured RemoteReadingBackend will be
            used by default.
        """
        self._backend = reading_backend or RemoteReadingBackend()

    @property
    def ru(self) -> Region:
        """Russian game region."""
        return Region(self._backend, uri=Path("ru"))

    @property
    def glob(self) -> Region:
        """Global game region. (NA, SEA, EU etc.)"""
        return Region(self._backend, uri=Path("global"))
