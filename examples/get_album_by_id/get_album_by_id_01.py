import os
from lapsepy.lapse import Lapse

if __name__ == '__main__':
    lapse = Lapse(refresh_token=os.getenv("REFRESH_TOKEN"))

    album_id = input("Album ID: ")

    album = lapse.get_album_by_id(album_id, last=10)

    for media in album.media:
        im = media.load()
        im.show()