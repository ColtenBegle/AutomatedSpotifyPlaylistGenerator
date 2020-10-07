import hashlib
import json
import requests
import base64
import webbrowser
import os
import re
import DataHelper
from requests.exceptions import HTTPError


def get_client_id():
    reader = open("%AppData%/.SECRET")
    try:
        json_secrets = json.load(reader)
    finally:
        reader.close()
    return json_secrets["client_id"]


class AuthorizationHelper:
    client_id = None
    redirect_uri = None
    code = None
    state = None
    code_verifier = None
    code_challenge = None

    def authorize(self):
        self.client_id = get_client_id()
        self.redirect_uri = "https://localhost/"
        self.code_verifier = self.get_code_verifier()
        self.code_challenge = self.get_code_challenge()
        self.state = self.get_state()
        self.code = self.get_code()
        request_data = self.get_access_token()
        return request_data


    def get_code_verifier(self):
        code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode('utf-8')
        code_verifier = re.sub('[^a-zA-Z0-9]+', '', code_verifier)
        return code_verifier

    def get_code_challenge(self):
        code_challenge = hashlib.sha256(self.code_verifier.encode('utf-8')).digest()
        code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8')
        code_challenge = code_challenge.replace('=', '')
        return code_challenge

    def get_state(self):
        state = base64.urlsafe_b64encode(os.urandom(60)).decode('utf-8')
        state = re.sub('[^a-zA-Z0-9]+', '', state)
        return state

    def get_code(self):
        scopes = "user-library-read user-library-modify playlist-read-collaborative " \
                 "playlist-modify-private playlist-modify-public playlist-read-private"

        query = f"https://accounts.spotify.com/authorize/?client_id={self.client_id}&" \
                f"response_type=code&redirect_uri={self.redirect_uri}&" \
                f"code_challenge_method=S256&code_challenge={self.code_challenge}&state={self.state}&scope={scopes}"
        try:
            response = requests.get(query)
            webbrowser.open(response.url)
            code = input("Enter code: ")
            state = input("Enter state: ")
            if state == self.state:
                return code
        except HTTPError as httpErr:
            print(httpErr)
            print(httpErr.strerror)
            return -1
        except KeyError as keyErr:
            # change this
            print(keyErr.__cause__)
            print(keyErr.args)
            return -1

    def get_headers(self):
        return {
            "Content-Type": "application/x-www-form-urlencoded"
        }

    def get_access_token(self):
        query = f"https://accounts.spotify.com/api/token/?client_id={self.client_id}&" \
                f"grant_type=authorization_code&code={self.code}&redirect_uri={self.redirect_uri}&" \
                f"code_verifier={self.code_verifier}"
        headers = self.get_headers()
        try:
            response = requests.post(query, headers=headers)
            response_data = response.json()
            return response_data
        except HTTPError as httpErr:
            print(httpErr)
            print(httpErr.strerror)
            return -1
        except KeyError as keyErr:
            print(response.status_code)
            print(response.reason)
            return -1
