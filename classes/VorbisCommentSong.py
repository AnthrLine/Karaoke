from classes.song import Song
from typing import List, Tuple

class VorbisCommentSong(Song):
    """Base class for FLAC and OGG, as both utilize Vorbis Comments."""

    def _get_tag(self, key: str) -> str:
        return self.audio.get(key, [""])[0]

    def title(self) -> str:
        return self._get_tag("title")

    def artist(self) -> str:
        return self._get_tag("artist")

    def album(self) -> str:
        return self._get_tag("album")

    def hasSLRC(self) -> bool:
        return "syncedlyrics" in self.audio

    def hasULRC(self) -> bool:
        return "lyrics" in self.audio

    def addULRC(self, lrc: str) -> None:
        self.audio["lyrics"] = lrc
        self.audio.save()

    def addSLRC(self, lrc: str) -> None:
        self.audio["syncedlyrics"] = lrc
        self.audio.save()