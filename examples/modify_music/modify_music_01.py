import os

from lapsepy import Lapse

if __name__ == '__main__':
    lapse = Lapse(os.getenv("REFRESH_TOKEN"))

    artist = input("Artist: ")
    artwork_url = input("Artwork URL: ")
    duration = int(input("Duration: "))
    song_title = input("Song Title: ")
    song_url = input("Song URL:")

    lapse.update_music(artist=artist, artwork_url=artwork_url, duration=duration,
                       song_title=song_title, song_url=song_url)
