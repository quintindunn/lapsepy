import os

from lapsepy.lapse import Lapse

if __name__ == '__main__':
    lapse = Lapse(os.getenv("REFRESH_TOKEN"))

    darkroom_media = lapse.query_darkroom()

    for content in darkroom_media:
        print(content.media_id)
        content.archive(lapse)
