import os
from PIL import Image
from lapsepy.lapse import Lapse

if __name__ == '__main__':
    lapse = Lapse(refresh_token=os.getenv("REFRESH_TOKEN"))
    upload_im = Image.open("../imgs/example_1.jpg")

    # Develop in 15 seconds
    friend_id = input("Friend UUID: ")
    lapse.upload_instant(im=upload_im, user_id=friend_id, caption="Automatic test")
