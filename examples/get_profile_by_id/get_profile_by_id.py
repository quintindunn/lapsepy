import os

from lapsepy.lapse import Lapse

if __name__ == '__main__':
    lapse = Lapse(os.getenv("REFRESH_TOKEN"))

    profile_id = input("Profile ID: ")

    profile = lapse.get_profile_by_id(profile_id)

    print(profile.username, profile.user_display_name)

    im = profile.load_profile_picture()
    im.show()
