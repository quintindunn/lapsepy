import os

from lapsepy.lapse import Lapse

if __name__ == '__main__':
    lapse = Lapse(os.getenv("REFRESH_TOKEN"))

    username_to_block = input("Username to block: ")

    user = lapse.get_profile_by_username(username_to_block)

    user.block(lapse)