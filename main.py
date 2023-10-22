"""
Author: Quintin Dunn
Date: 10/22/23
"""

import os
from PIL import Image

from lapsepy import Journal
from lapsepy import refresh


if __name__ == '__main__':
    token = refresh(os.getenv("REFRESH_TOKEN"))
    journal = Journal(authorization=token)
    # im_ = Image.open("./examples/imgs/example_1.jpg")
    # journal.upload_photo(im_, 10)
    journal.get_friends_feed(count=10)