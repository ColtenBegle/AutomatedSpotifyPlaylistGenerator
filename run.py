"""
Programmer: Colten Begle    Date: 9/10/2020
Description: This program generates playlists from your liked songs based
on the genre of music using the Spotify Web API
"""
import datetime
import json
import DataHelper
from SpotifyUser import SpotifyUser
from AccessToken import AccessToken


def get_playlist_id(playlist_data, playlist_name):
    playlists = []
    items = playlist_data["items"]
    for playlist in items:
        playlists.append(playlist)
    for playlist in playlists:
        if playlist["name"] == playlist_name:
            playlist_id = playlist["id"]
            return playlist_id
    return -1


def run():
    with open("test.json", "r") as f:
        playlist_data = json.load(f)
        playlist_id = get_playlist_id(playlist_data, "Dana")
        print(playlist_id)
    # name = input("Enter your Spotify username: ")
    # user = SpotifyUser(name)
    #
    # user.get_user_playlists()
    # print(user.playlist_data)


if __name__ == '__main__':
    run()
