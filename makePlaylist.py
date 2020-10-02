"""
Programmer: Colten Begle    Date: 9/10/2020
Description: This program generates playlists from your liked songs based
on the genre of music using the Spotify Web API
"""
import json
import requests
import base64
import datetime
import hashlib
import os
import re
from requests.exceptions import HTTPError


class SpotifyUser:
    user_id = None
    access_token = None
    profile_data = None
    playlist_data = None

    def __init__(self, user_id, access_token):
        self.user_id = user_id
        self.access_token = "BQB3quR9JFio3OWtIG9iZTCdSJtmTis5beGLmrCNP-8b75dbqUktT-EhUE2lsXktkSCf36Jbdw5HNldclcTwYVWmUinkcrTveV7L60kmpt9u_SKX4LyvkJ795jeMsSE06DtEfSJzFn4Xd-TDXuSxu3Soznf93wu0iE3Tw8tRlzSYbybrPJ9-H5dYZTFhwX4kNZuGORA"

    def get_user_profile(self):
        query = "https://api.spotify.com/v1/users/{}".format(self.user_id)
        headers = self.get_headers()
        response = requests.get(query, headers=headers)
        self.profile_data = response.json()

    def get_user_playlists(self):
        query = "https://api.spotify.com/v1/users/{}/playlists".format(self.user_id)
        headers = self.get_headers()
        response = requests.get(query, headers=headers)
        self.playlist_data = response.json()

    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def create_playlist(self, name, description="", public=True):
        query = "https://api.spotify.com/v1/users/{}/playlists".format(self.user_id)
        headers = self.get_headers()
        request_body = json.dumps({
            "name": f"{name}",
            "description": f"{description}",
            "public": f"{public}"
        })
        try:
            response = requests.post(query, data=request_body, headers=headers)
            json_data = response.json()
            return json_data["id"]
        except HTTPError as httpErr:
            print(response.status_code)
            print(response.reason)
            return -1
        except KeyError as keyErr:
            print(response.status_code)
            print(response.reason)
            return -1


class SpotifyInterface:
    client_id = None
    client_secret = None
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    code_verifier = None
    code_challenge = None

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    # Old auth code
    # def authorize(self):
    #     # do lookup for a token
    #     # this token is for future requests
    #     query = 'https://accounts.spotify.com/api/token'
    #     token_data = self.get_token_data()
    #     token_headers = self.get_token_headers()
    #     scopes = json.dumps([
    #         "playlist-read-collaborative",
    #         "playlist-modify-public",
    #         "user-library-modify",
    #         "user-top-read",
    #         "playlist-read-private",
    #         "playlist-modify-private",
    #         "user-library-read"
    #     ])
    #     params = json.dumps({
    #         "scope": f"{scopes}"
    #     })
    #     try:
    #         response = requests.post(query, params=params, data=token_data, headers=token_headers)
    #
    #         response.raise_for_status()
    #     except HTTPError as http_err:
    #         print(f'HTTP error occurred: {http_err}')
    #         return False
    #     except Exception as err:
    #         print(f'Other error occurred: {err}')
    #         return False
    #     else:
    #         token_response_data = response.json()
    #         response = datetime.datetime.now()
    #         self.access_token = token_response_data['access_token']
    #         expires_in = token_response_data['expires_in']
    #         self.access_token_expires = response + datetime.timedelta(seconds=expires_in)
    #         self.access_token_did_expire = self.access_token_expires < response
    #         return True
    #
    # def get_token_headers(self):
    #     client_cred = self.encode_cred()
    #     return {
    #         "Authorization": f"Basic {client_cred.decode()}"
    #     }
    #
    # def get_token_data(self):
    #     token_data = {"grant_type": "client_credentials"}
    #     return token_data
    #
    # def encode_cred(self):
    #     client_cred = f'{self.client_id}:{self.client_secret}'
    #     client_cred_b64 = base64.b64encode(client_cred.encode())
    #     return client_cred_b64

    # New auth code for PKCY
    def authroize(self):
        query = "https://accounts.spotify.com/authorize"
        state = base64.urlsafe_b64encode(os.urandom(60)).decode('utf-8')
        state = re.sub('[^a-zA-Z0-9]+', '', state)
        scopes = json.dump([
            "playlist-read-collaborative",
            "playlist-modify-public",
            "user-library-modify",
            "user-top-read",
            "playlist-read-private",
            "playlist-modify-private",
            "user-library-read"
        ])
        params = json.dump({
            "client_id": f"{self.client_id}",
            "response_type": "code",
            "redirect_uri": "https://localhost/",
            "code_challenge_method": "S256",
            "code_challenge": f"{self.code_challenge}",
            "state": f"{state}",
            "scope": f"{scopes}"
        })
        response = requests.get(query, params=params)
        return response

    def gen_code_verifier(self):
        code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode('utf-8')
        code_verifier = re.sub('[^a-zA-Z0-9]+', '', code_verifier)
        return code_verifier

    def gen_code_challenge(self):
        code_challenge = hashlib.sha256(self.code_verifier.encode('utf-8')).digest()
        code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8')
        code_challenge = code_challenge.replace('=', '')
        return code_challenge


interface = SpotifyInterface('24f3734a2acc41eb93651ce7b4bf1d8f',
                             '38092d7194cc4ac098c2bd15eb9370d8')
# interface.authorize()
# #interface.gen_code_verifier()
# #interface.gen_code_challenge()

user = SpotifyUser("coltbo", interface.access_token)
user.create_playlist("test2")

