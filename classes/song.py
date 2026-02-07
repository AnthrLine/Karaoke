import mutagen
from mutagen.id3 import ID3, USLT, SYLT, ID3TimeStamp

class Song:

    # CONSTRUCTOR ######################################################################################################
    def __init__(self, filename: str) -> None:
        self._filename: str = filename

        audio = ID3(self._filename)

        self._title: str = audio.get("TIT2", [""])[0]
        self._artist: str = audio.get("TPE2", [""])[0]
        self._album: str = audio.get("TALB", [""])[0]

        self._has_unsynced_lyrics = "USLT" in audio
        self._has_synced_lyrics = "SYLT" in audio

    # GETTERS ##########################################################################################################
    def getTitle(self) -> str:
        return self._title

    def getArtist(self) -> str:
        return self._artist

    def getAlbum(self) -> str:
        return self._album

    def getFilename(self) -> str:
        return self._filename

    def hasSLRC(self) -> bool:
        return self._has_synced_lyrics

    def hasULRC(self) -> bool:
        return self._has_unsynced_lyrics

    # SETTERS ##########################################################################################################

    def setULRC(self, lrc: str) -> None:
        audio = ID3(self._filename)

        audio.add(USLT(
            desc='Lyrics',
            text=lrc
        ))

        # Save the changes
        audio.save()

    def setSLRC(self, lrc) -> None:
        audio = ID3(self._filename)

        sylt_frame = SYLT(
            format=1,  # Format: 1 for time-stamped lyrics
            type=1,  # Type: 1 for lyrics
            desc='Synced Lyrics',
            text=[]
        )

        # Add each lyric and its timestamp
        for timestamp, lyric in lrc:
            sylt_frame.text.append((ID3TimeStamp(timestamp), lyric))

        # Add the SYLT frame to the audio file
        audio.add(sylt_frame)

        # Save the changes
        audio.save()