from mutagen.id3 import USLT, ID3TimeStamp, SYLT
from mutagen.mp3 import MP3
from typing import List, Tuple

from classes.song import Song

class MP3Song(Song):
    def __init__(self, filename: str) -> None:
        super().__init__(filename)
        self.audio = MP3(self._filename)
        if self.audio.tags is None:
            self.audio.add_tags()

    def title(self) -> str:
        return self.audio.tags.get("TIT2", [""])[0] if "TIT2" in self.audio.tags else ""

    def artist(self) -> str:
        return self.audio.tags.get("TPE2", [""])[0] if "TPE2" in self.audio.tags else ""

    def album(self) -> str:
        return self.audio.tags.get("TALB", [""])[0] if "TALB" in self.audio.tags else ""

    def hasSLRC(self) -> bool:
        return any(key.startswith("SYLT") for key in self.audio.tags.keys())

    def hasULRC(self) -> bool:
        return any(key.startswith("USLT") for key in self.audio.tags.keys())

    def addULRC(self, lrc: str) -> None:
        self.audio.tags.add(USLT(desc='Lyrics', text=lrc))
        self.audio.save()

    def addSLRC(self, lrc: str) -> None:
        sylt_frame = SYLT(format=1, type=1, desc='Synced Lyrics', text=[])

        # Parse the raw LRC string into timestamps for the ID3 frame
        parsed_timestamps = Song.parse_lrc_to_ms(lrc)
        for timestamp_ms, lyric in parsed_timestamps:
            sylt_frame.text.append((ID3TimeStamp(timestamp_ms), lyric))

        self.audio.tags.add(sylt_frame)
        self.audio.save()