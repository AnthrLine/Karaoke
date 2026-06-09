from classes.VorbisCommentSong import VorbisCommentSong
from mutagen.oggvorbis import OggVorbis

class OGGSong(VorbisCommentSong):
    def __init__(self, filename: str) -> None:
        super().__init__(filename)
        self.audio = OggVorbis(self._filename)