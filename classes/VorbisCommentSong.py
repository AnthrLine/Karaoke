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

    def addSLRC(self, lrc: List[Tuple[int, str]]) -> None:
        # Vorbis does not have a native binary synced format like ID3.
        # It relies on formatting an LRC string directly into a tag.
        lrc_string = "\n".join([f"[{timestamp}] {lyric}" for timestamp, lyric in lrc])
        self.audio["syncedlyrics"] = lrc_string
        self.audio.save()