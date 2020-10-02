"""
Programmer: Colten Begle    Date: 9/10/2020
Description: This program generates playlists from your liked songs based
on the genre of music using the Spotify Web API
"""
import DataHelper
from SpotifyUser import SpotifyUser
from AccessToken import AccessToken


def run():
    name = input("Enter your Spotify username: ")
    access_token = DataHelper.get_good_access_token(name)
    if not (access_token is None):
        print(access_token.user_id, access_token.token, access_token.token_type, access_token.expires_in, access_token.scope)
    # user = SpotifyUser(name)
    # print(user.access_token)
    # print(user.access_token.token)


if __name__ == '__main__':
    run()
