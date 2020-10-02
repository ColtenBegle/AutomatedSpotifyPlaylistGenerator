"""
Programmer: Colten Begle    Date: 9/10/2020
Description: This program generates playlists from your liked songs based
on the genre of music using the Spotify Web API
"""
from SpotifyUser import SpotifyUser


def run():
    name = input("Enter your Spotify username: ")
    user = SpotifyUser(name)
    print(user.access_token)
    print(user.access_token.token)


if __name__ == '__main__':
    run()
