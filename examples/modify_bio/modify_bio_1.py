import os

from lapsepy import Lapse

if __name__ == '__main__':
    lapse = Lapse(os.getenv("REFRESH_TOKEN"))

    bio = input("New Bio: ")
    lapse.update_bio(bio)
