"""
Author: Quintin Dunn
Date: 10/22/23
"""

import os
import sys

from lapsepy.lapse import Lapse

import logging

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

if __name__ == '__main__':
    lapse = Lapse(os.getenv("REFRESH_TOKEN"))

    friends_feed = lapse.get_friends_feed(count=20)

    for profile in friends_feed:
        print(profile.username)
        for snap in profile.media:
            snap.load_snap(quality=100, fl_keep_iptc=True)
            snap.filtered.save(snap.filtered_id.replace("/", "") + ".jpg")
