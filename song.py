import mutagen

class Song:
    def __init__(self, filename: str) -> None:
        self.filename = filename

        metadata = mutagen.File(self.filename)

        self.title = metadata["title"]
        self.artist = metadata["artist"]
        self.album = metadata["album"]