import os
from PIL import Image
from lapsepy.lapse import Lapse

if __name__ == '__main__':
    lapse = Lapse(refresh_token=os.getenv("REFRESH_TOKEN"))
    upload_im = Image.open("../imgs/example_1.jpg")

    friend_id = input("Friend UUID: ")

    # Get friend object
    friend = lapse.get_profile_by_id(friend_id)

    lapse.upload_instant(im=upload_im, user=friend, caption="Automatic test")
