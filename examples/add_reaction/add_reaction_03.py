import os
from lapsepy.lapse import Lapse

if __name__ == '__main__':
    lapse = Lapse(refresh_token=os.getenv("REFRESH_TOKEN"))

    feed = lapse.get_friends_feed(count=5)

    for friend_node in feed:
        friend = friend_node.profile

        for entry in friend_node.entries:
            entry.load_snap()

            im = entry.filtered
            im.show(title=friend.user_display_name)
            if input(f"{friend.user_display_name}, react? (y/n) ") == "y":
                entry.react(ctx=lapse, reaction=input("Reaction: "))
