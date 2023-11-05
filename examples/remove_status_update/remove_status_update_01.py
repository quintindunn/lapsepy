import os

from lapsepy import Lapse

if __name__ == '__main__':
    lapse = Lapse(os.getenv("REFRESH_TOKEN"))

    msg_to_remove = input("MSG ID: ")
    lapse.remove_status_update(msg_to_remove)
