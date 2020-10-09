import json
import requests
from AuthorizationHelper import AuthorizationHelper
from AccessToken import AccessToken
import math
from requests.exceptions import HTTPError

from Playlist import Playlist
from Song import Song


def get_songs(song_data):
    songs = []
    dict_songs = json.loads(song_data)
    items = dict_songs["items"]
    for item in items:
        track = item["track"]
        song_id = track["id"]
        song_uri = track["uri"]
        song_name = track["name"]
        album = track["album"]
        release_date = album["release_date"]
        song = Song(song_id, song_uri, song_name, release_date)
        songs.append(song)
    return songs


class SpotifyUser:
    user_id = None
    code_verifier = None
    code_challenge = None
    access_token = None
    token_data = None
    AuthHelper = None
    playlists = None

    def __init__(self, user_id):
        self.user_id = user_id
        self.AuthHelper = AuthorizationHelper()
        self.token_data = self.AuthHelper.authorize()
        self.access_token = AccessToken(user_id, self.token_data)
        self.playlists = self.get_user_playlists()

    def get_user_profile(self):
        query = "https://api.spotify.com/v1/users/{}".format(self.user_id)
        headers = self.get_headers()
        response = requests.get(query, headers=headers)
        return response.json()

    def get_user_playlists(self):
        query = "https://api.spotify.com/v1/users/{}/playlists".format(self.user_id)
        headers = self.get_headers()
        response = requests.get(query, headers=headers)
        playlist_data = json.loads(response.json())
        playlists = self.get_playlists(playlist_data)
        return playlists

    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.access_token.token}",
            "Content-Type": "application/json"
        }

    def get_playlists(self, playlist_data):
        playlists = []
        items = playlist_data["items"]
        for item in items:
            playlist_id = item["id"]
            name = item["name"]
            description = item["description"]
            tracks = item["tracks"]
            track_count = tracks["total"]
            public = item["public"]
            songs = self.get_playlist_content(playlist_id, track_count)
            playlist = Playlist(name, description, track_count, songs, public, playlist_id)
            playlists.append(playlist)
        return playlists

    def get_playlist_content(self, playlist_id, offset=0):
        songs = []
        if offset > 100:
            times_greater = offset / 100
            offset = 0
            for i in range(math.ceil(times_greater)):
                query = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?offset={offset}"
                headers = self.get_headers()
                response = requests.get(query, headers=headers)
                response_json = response.json()
                songs += get_songs(response_json)
                offset += 100
        return songs
