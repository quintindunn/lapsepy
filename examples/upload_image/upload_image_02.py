import os
import time

from PIL import Image
from lapsepy.lapse import Lapse

if __name__ == '__main__':
    lapse = Lapse(refresh_token=os.getenv("REFRESH_TOKEN"))
    upload_im = Image.open("../imgs/example_1.jpg")

    # Develop in 15 seconds
    darkroom_snap = lapse.upload_photo(im=upload_im, develop_in=5)

    review = darkroom_snap.reviewed

    while darkroom_snap.developed is False:
        time.sleep(0.5)

    lapse.review_snaps(archived=[review])

