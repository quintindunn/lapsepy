import os

from lapsepy.lapse import Lapse

if __name__ == '__main__':
    lapse = Lapse(os.getenv("REFRESH_TOKEN"))

    darkroom_media = lapse.query_darkroom()

    if not os.path.isdir("./out"):
        os.mkdir("./out")

    for content in darkroom_media:
        # Load the image
        im = content.load()

        # Save the image
        im.save(f"./out/{content.media_id}.jpeg", format="jpeg")
