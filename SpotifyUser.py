import json
import requests
from AuthorizationHelper import AuthorizationHelper
from AccessToken import AccessToken
import base64
import webbrowser
import datetime
import hashlib
import os
import re
from requests.exceptions import HTTPError


class SpotifyUser:
    user_id = None
    code_verifier = None
    code_challenge = None
    access_token = None
    token_data = None
    profile_data = None
    playlist_data = None
    AuthHelper = None

    def __init__(self, user_id):
        self.user_id = user_id
        self.AuthHelper = AuthorizationHelper()
        self.token_data = self.AuthHelper.authorize()
        self.access_token = AccessToken(self.token_data)

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
            "Authorization": f"Bearer {self.access_token.token}",
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
