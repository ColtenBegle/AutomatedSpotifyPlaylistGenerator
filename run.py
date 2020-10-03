"""
Programmer: Colten Begle    Date: 9/10/2020
Description: This program generates playlists from your liked songs based
on the genre of music using the Spotify Web API
"""
import datetime

import DataHelper
from SpotifyUser import SpotifyUser
from AccessToken import AccessToken


def run():
    name = input("Enter your Spotify username: ")
    token_data = {
        "access_token": "dasdfjajdfj23203",
        "token_type": "credential",
        "expires_in": "2025-10-02 23:59:59",
        "refresh_token": "dfajslkdjflaksj",
        "scope": ["Hello", "world"]
    }
    access_token = AccessToken(name, token_data)
    DataHelper.store_access_token(access_token)
    if not (access_token is None):
        print(access_token.user_id, access_token.token, access_token.token_type,
              access_token.expires_in, access_token.scope)
    else:
        print(f"No access tokens found for user: {name}")
    # user = SpotifyUser(name)
    # print(user.access_token)
    # print(user.access_token.token)


if __name__ == '__main__':
    run()
