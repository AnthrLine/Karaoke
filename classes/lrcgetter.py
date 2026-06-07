from classes import song
import requests

class lrcgetter:

    # CONSTRUCTOR ######################################################################################################
    def __init__(self, track):
        self._track = track

    # GETTERS ##########################################################################################################
    def _getCompleteData(self):
        # Http request params:
        payload = {
            'track_name': self._track.title(),
            'artist_name': self._track.artist(),
            'album_name': self._track.album(),
            'duration': self._track.length()
        }

        r = requests.get('https://lrclib.net/api/get', params=payload)
        return r

    def searchSong(self) -> bool:

        if self._track.artist() != "" and self._track.title() != "" and self._track.album() != "" and self._track.length() != -1:



        print(r.text)

        return True

