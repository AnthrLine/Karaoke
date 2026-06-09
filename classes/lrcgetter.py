from typing import Tuple

from classes import song
import requests

from classes.song import Song


class Lrcgetter:

    @staticmethod
    def _getCompleteData(track: Song):
        # Http request params:
        payload = {
            'track_name': track.title(),
            'artist_name': track.artist(),
            'album_name': track.album(),
            'duration': track.length()
        }

        r = requests.get('https://lrclib.net/api/get', params=payload)

        if r.status_code == 404:
            # remove album and retry once
            payload.pop('album_name', None)
            r = requests.get('https://lrclib.net/api/get', params=payload)

        return r

    @staticmethod
    def searchSong(track: Song) -> Tuple[str, str]:

        r = Lrcgetter._getCompleteData(track)

        ULRC : str = r.json().get('plainLyrics')
        SLRC : str = r.json().get('syncedLyrics')

        return ULRC, SLRC

