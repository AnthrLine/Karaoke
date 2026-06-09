from classes.VorbisCommentSong import VorbisCommentSong
from mutagen.flac import FLAC

class FLACSong(VorbisCommentSong):
    def __init__(self, filename: str) -> None:
        super().__init__(filename)
        self.audio = FLAC(self._filename)