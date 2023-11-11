import os

from lapsepy.lapse import Lapse

if __name__ == '__main__':
    lapse = Lapse(os.getenv("REFRESH_TOKEN"))

    username = input("Username: ")

    profile = lapse.get_profile_by_username(username, friends_limit=1)

    print(profile.username, profile.user_display_name)

    im = profile.load_profile_picture()
    im.show()
