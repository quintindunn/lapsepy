import os
from lapsepy.lapse import Lapse

if __name__ == '__main__':
    lapse = Lapse(refresh_token=os.getenv("REFRESH_TOKEN"))

    msg_id = input("Message ID: ")
    comment = input("Comment: ")

    lapse.send_comment(msg_id=msg_id, text=comment)
