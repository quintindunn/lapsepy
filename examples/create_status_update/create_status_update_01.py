import os

from lapsepy.lapse import Lapse

if __name__ == '__main__':
    lapse = Lapse(os.getenv("REFRESH_TOKEN"))

    msg = input("Message: ")
    lapse.create_status_update(text=msg)
