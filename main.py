"""
Author: Quintin Dunn
Date: 10/22/23
"""


import os
from PIL import Image

from lapsepy import Journal


if __name__ == '__main__':
    journal = Journal(authorization=os.getenv("TOKEN"))
    im_ = Image.open("./examples/imgs/example_1.jpg")
    journal.upload_photo(im_, 10)
