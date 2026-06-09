import os

import mutagen
from abc import ABC, abstractmethod
from typing import List, Tuple, MutableMapping, Type


class Song(ABC):
    """Abstract base class for audio files."""

    def __init__(self, filename: str) -> None:
        self._filename: str = filename

        # mutagen.File generically reads standard audio properties
        audio = mutagen.File(self._filename)
        if audio is None:
            raise ValueError(f"Unsupported or corrupted audio file: {filename}")

        # Duration is universally accessible via info.length across all mutagen formats
        self._length: int = int(audio.info.length)

    @staticmethod
    def get_format_registry() -> MutableMapping[str, Type['Song']]:
        """Returns a mutable map linking file extensions to their handlers."""
        # Deferring the references inside the method ensures the subclasses
        # are fully loaded into memory before this dictionary is constructed.
        from classes.MP3Song import MP3Song
        from classes.FLACSong import FLACSong
        from classes.OGGSong import OGGSong
        from classes.WAVSong import WAVSong

        return {
            ".mp3": MP3Song,
            ".flac": FLACSong,
            ".ogg": OGGSong,
            ".wav": WAVSong
        }

    @classmethod
    def from_file(cls, filename: str) -> 'Song':
        """Factory method to automatically instantiate the correct Song subclass."""
        _, ext = os.path.splitext(filename)
        registry = cls.get_format_registry()

        handler_class = registry.get(ext.lower())
        if not handler_class:
            raise ValueError(f"Unsupported file extension: {ext}")

        return handler_class(filename)

    def filename(self) -> str:
        return self._filename

    def length(self) -> int:
        return self._length

    @abstractmethod
    def title(self) -> str:
        pass

    @abstractmethod
    def artist(self) -> str:
        pass

    @abstractmethod
    def album(self) -> str:
        pass

    @abstractmethod
    def hasSLRC(self) -> bool:
        pass

    @abstractmethod
    def hasULRC(self) -> bool:
        pass

    @abstractmethod
    def addULRC(self, lrc: str) -> None:
        pass

    @abstractmethod
    def addSLRC(self, lrc: List[Tuple[int, str]]) -> None:
        pass