import os
import re

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

    @staticmethod
    def parse_lrc_to_ms(lrc_string: str) -> List[Tuple[int, str]]:
        """Parses a standard LRC string into a list of (timestamp_ms, lyric) tuples."""
        parsed = []
        # Matches [mm:ss.xx], [mm:ss:xx], or [mm:ss]
        pattern = re.compile(r'\[(\d+):(\d+)(?:[.:](\d+))?](.*)')

        for line in lrc_string.splitlines():
            match = pattern.match(line.strip())
            if match:
                minutes = int(match.group(1))
                seconds = int(match.group(2))
                fraction = match.group(3)
                lyric = match.group(4).strip()

                # Convert fraction (usually 2-digit centiseconds) to milliseconds
                ms = 0
                if fraction:
                    if len(fraction) == 2:
                        ms = int(fraction) * 10
                    elif len(fraction) == 3:
                        ms = int(fraction)

                total_ms = (minutes * 60 + seconds) * 1000 + ms
                parsed.append((total_ms, lyric))

        return parsed

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
    def addSLRC(self, lrc: str) -> None:
        pass