"""
Programmer: Colten Begle    Date: 9/10/2020
Description: This program generates playlists from your liked songs based
on the genre of music using the Spotify Web API
"""
import datetime
from Spotify.Playlist import Playlist
from Spotify.SpotifyUser import SpotifyUser


def main():
    name = input("Enter your Spotify username: ")
    user = SpotifyUser(name)

    date_old = datetime.datetime(1980, 1, 1)
    old_songs = []
    songs_80s = []
    date90s = datetime.datetime(1990, 1, 1)
    songs_90s = []
    date2000s = datetime.datetime(2000, 1, 1)
    songs_2000s = []
    date2010s = datetime.datetime(2010, 1, 1)
    songs_2010s = []
    date2020s = datetime.datetime(2020, 1, 1)
    songs_2020s = []

    playlist = user.playlists["Liked Songs Test"]
    for song in playlist.songs:
        year = song.song_release_date[0:4]
        release_date = datetime.datetime.strptime(year, "%Y")
        if release_date < date_old:
            old_songs.append(song)
        elif release_date < date90s:
            songs_80s.append(song)
        elif release_date < date2000s:
            songs_90s.append(song)
        elif release_date < date2010s:
            songs_2000s.append(song)
        elif release_date < date2020s:
            songs_2010s.append(song)
        else:
            songs_2020s.append(song)
    if len(old_songs) > 0:
        new_playlist = Playlist("Old Songs", client=user)
        new_playlist.add_songs_to_playlist(old_songs, user)
    if len(songs_80s) > 0:
        new_playlist = Playlist("80's Songs", client=user)
        new_playlist.add_songs_to_playlist(songs_80s, user)
    if len(songs_90s) > 0:
        new_playlist = Playlist("90's Songs", client=user)
        new_playlist.add_songs_to_playlist(songs_90s, user)
    if len(songs_2000s) > 0:
        new_playlist = Playlist("2000's Songs", client=user)
        new_playlist.add_songs_to_playlist(songs_2000s, user)
    if len(songs_2010s) > 0:
        new_playlist = Playlist("2010's Songs", client=user)
        new_playlist.add_songs_to_playlist(songs_2010s, user)
    if len(songs_2020s) > 0:
        new_playlist = Playlist("2020's Songs", client=user)
        new_playlist.add_songs_to_playlist(songs_2020s, user)


if __name__ == '__main__':
    main()
