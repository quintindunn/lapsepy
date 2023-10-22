"""
Author: Quintin Dunn
Date: 10/22/23
"""

import os

from lapsepy.lapse import Lapse


if __name__ == '__main__':
    lapse = Lapse(os.getenv("REFRESH_TOKEN"))

    friends_feed = lapse.get_friends_feed()

    print(friends_feed)
