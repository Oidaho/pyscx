from pathlib import Path

from pyscx.database import ReadingBackend, RemoteReadingBackend
from pyscx.models.database import GameItem

from ._builder import Region
from .backends import JsonDeserializer


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
        self._default_deserializer = JsonDeserializer[GameItem](GameItem)

    @property
    def glob(self) -> Region:
        """Global game region. (NA, SEA, EU etc.)"""
        return Region(self._backend, self._default_deserializer, uri=Path("global"))

    @property
    def ru(self) -> Region:
        """Russian game region."""
        return Region(self._backend, self._default_deserializer, uri=Path("ru"))

    @property
    def eu(self) -> Region:
        """European game region."""
        return self.glob

    @property
    def na(self) -> Region:
        """North American game region."""
        return self.glob

    @property
    def sea(self) -> Region:
        """Southeast Asian game region."""
        return self.glob

    @property
    def nea(self) -> Region:
        """Northeast Asian game region."""
        return self.glob
