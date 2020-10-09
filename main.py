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
from Song import Song


def main():
    name = input("Enter your Spotify username: ")
    user = SpotifyUser(name)




if __name__ == '__main__':
    main()
