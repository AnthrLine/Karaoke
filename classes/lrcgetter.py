import song
import requests

class LrcGetter:

    # CONSTRUCTOR ######################################################################################################
    def __init__(self, track):
        self._track = track

    # GETTERS ##########################################################################################################
    def searchSong(self) -> bool:

        # Http request params:
        payload = {
            'track_name': self._track.getTitle(),
            'artist_name': self._track.getArtist(),
            'album_name': self._track.getAlbum(),
            'duration': self._track.getLength()
        }

        r = requests.get('https://lrclib.net/api/get', params=payload)

        print(r.text)

        return True