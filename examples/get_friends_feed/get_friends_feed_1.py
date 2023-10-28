import os

from lapsepy.lapse import Lapse

if __name__ == '__main__':
    lapse = Lapse(os.getenv("REFRESH_TOKEN"))

    # DOESN'T RETURN 20 IMAGES, GETS 20 COLLECTIONS
    friends_feed = lapse.get_friends_feed(count=20)

    if not os.path.isdir("./out"):
        os.mkdir("./out")

    for friend_node in friends_feed:
        profile = friend_node.profile
        profile.load_profile_picture(quality=100, height=None)
        profile.profile_picture.save(f"./out/{profile.username}.jpg")
        for entry in friend_node.entries:
            entry.load_snap(quality=100, fl_keep_iptc=True)
            save_path = f"./out/{entry.filtered_id.replace('/', '_')}.jpg"
            entry.filtered.save(save_path)

