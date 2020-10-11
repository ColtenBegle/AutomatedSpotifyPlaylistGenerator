class Song:
    song_id = None
    song_uri = None
    song_name = None
    song_release_date = None

    def __init__(self, song_id, song_uri, song_name, song_release_date):
        self.song_id = song_id
        self.song_uri = song_uri
        self.song_name = song_name
        self.song_release_date = song_release_date
