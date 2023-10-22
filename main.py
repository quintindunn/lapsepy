import os
from PIL import Image

from lapsepy.journal import journal


if __name__ == '__main__':
    journal = journal.Journal(authorization=os.getenv("TOKEN"))
    im_ = Image.open("./examples/imgs/example_1.jpg")
    journal.upload_photo(im_, 10)
