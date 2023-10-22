import os

from lapsepy.lapse import Lapse

if __name__ == '__main__':
    lapse = Lapse(os.getenv("REFRESH_TOKEN"))

    # DOESN'T RETURN 20 IMAGES, GETS 20 COLLECTIONS
    friends_feed = lapse.get_friends_feed(count=20)

    if not os.path.isdir("./out"):
        os.mkdir("./out")

    for profile in friends_feed:

        print(profile.username)
        for snap in profile.media:
            snap.load_snap(quality=100, fl_keep_iptc=True)
            save_path = f"./out/{snap.filtered_id.replace('/', '_')}.jpg"
            snap.filtered.save(save_path)
