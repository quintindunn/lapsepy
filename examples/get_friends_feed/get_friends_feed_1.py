import os

import requests.exceptions

from lapsepy.lapse import Lapse

if __name__ == '__main__':
    lapse = Lapse(os.getenv("REFRESH_TOKEN"))

    # DOESN'T RETURN 20 IMAGES, GETS 20 COLLECTIONS
    friends_feed = lapse.get_friends_feed(count=20)

    if not os.path.isdir("./out"):
        os.mkdir("./out")

    for friend_node in friends_feed:
        profile = friend_node.profile

        # Get profile picture
        try:
            profile.load_profile_picture(quality=100, height=None)
            profile.profile_picture.save(f"./out/{profile.username}.jpg")
        except requests.exceptions.HTTPError:
            print(f"Failed getting profile picture for {profile.username}")

        # Get all images from collections
        for entry in friend_node.entries:
            entry.load_snap(quality=100, fl_keep_iptc=True)
            save_path = f"./out/{entry.filtered_id.replace('/', '_')}.jpg"
            entry.filtered.save(save_path)

        # Get profile music if user has profile music.
        if profile.profile_music is not None:
            profile.profile_music.load()
            profile_music = profile.profile_music

            # Save artwork if exists
            if profile_music.artwork:
                save_path = f"./out/{profile.username}_music.png"
                profile_music.artwork.save(save_path)

            # Save song
            save_path = f"./out/{profile.username}_music.mp3"
            with open(save_path, 'wb') as f:
                f.write(profile_music.song)
