import json
import requests
from requests.exceptions import HTTPError


class Playlist:
    playlist_id = None
    playlist_name = None
    songs = None

    def __init__(self, playlist_id, playlist_name, songs=[]):
        self.playlist_id = playlist_id
        self.playlist_name = playlist_name
        self.songs = songs

    def create_playlist(self, client, name, description="", public=True):
        query = "https://api.spotify.com/v1/users/{}/playlists".format(client.user_id)
        headers = client.get_headers()
        request_body = json.dumps({
            "name": f"{name}",
            "description": f"{description}",
            "public": f"{public}"
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
            print(response.status_code)
            print(response.reason)
            return -1
