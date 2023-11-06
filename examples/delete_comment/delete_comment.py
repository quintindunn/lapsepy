import os
from lapsepy.lapse import Lapse

if __name__ == '__main__':
    lapse = Lapse(refresh_token=os.getenv("REFRESH_TOKEN"))

    msg_id = input("Message ID: ")
    comment = input("Comment: ")

    lapse.delete_comment(msg_id=msg_id, comment_id=comment)
