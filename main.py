"""
Author: Quintin Dunn
Date: 10/22/23
"""

import os

from lapsepy.lapse import Lapse


if __name__ == '__main__':
    lapse = Lapse(os.getenv("REFRESH_TOKEN"))

    friends_feed = lapse.get_friends_feed(count=20)

    for profile in friends_feed:
        for snap in profile.media:
            snap.load_snap(quality=100, fl_keep_iptc=True)
            snap.filtered.save(snap.filtered_id.replace("/", "") + ".jpg")