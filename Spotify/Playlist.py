import json
import math
import requests
from requests.exceptions import HTTPError
from itertools import islice


def to_json_array(songs):
    song_uris = []
    for song in songs:
        song_uris.append(song.song_uri)
    json_array = json.dumps(song_uris)
    return json_array


class Playlist:
    playlist_id = None
    name = None
    description = None
    track_count = None
    songs = None
    public = None

    def __init__(self, playlist_name, description="", track_count=0, songs=None,
                 public=True, playlist_id=None, client=None):
        self.name = playlist_name
        self.description = description
        self.track_count = track_count
        self.songs = songs
        self.public = public
        if playlist_id is None and not (client is None):
            self.playlist_id = self.create_playlist(client)
        else:
            self.playlist_id = playlist_id

    def create_playlist(self, client):
        query = "https://api.spotify.com/v1/users/{}/playlists".format(client.user_id)
        headers = client.get_headers()
        request_body = json.dumps({
            "name": f"{self.name}",
            "description": f"{self.description}",
            "public": f"{self.public}"
        })
        try:
            response = requests.post(query, data=request_body, headers=headers)
            response_data = response.json()
            return response_data['id']
        except HTTPError as httpErr:
            print(httpErr)
            print(httpErr.strerror)
            return -1
        except KeyError as keyErr:
            print(keyErr)
            return -1

    def add_songs_to_playlist(self, songs, client):
        responses = []
        if len(songs) > 100:
            times_greater = len(songs) / 100
            songs_remaining = len(songs)
            cutoff = 100
            prev_cutoff = 0
            for i in range(math.ceil(times_greater)):
                temp_songs = list(islice(songs, prev_cutoff, cutoff))
                query = f"https://api.spotify.com/v1/playlists/{self.playlist_id}/tracks"
                headers = client.get_headers()
                uris = to_json_array(temp_songs)
                response = requests.post(query, data=uris, headers=headers)
                response_data = response.json()
                responses.append(response_data)
                songs_remaining -= (cutoff - prev_cutoff)
                if songs_remaining < 100:
                    prev_cutoff = cutoff
                    cutoff += songs_remaining
                else:
                    prev_cutoff = cutoff
                    cutoff += 100
        else:
            query = f"https://api.spotify.com/v1/playlists/{self.playlist_id}/tracks"
            headers = client.get_headers()
            uris = to_json_array(songs)
            response = requests.post(query, data=uris, headers=headers)
            response_data = response.json()
            responses.append(response_data)

        return responses

