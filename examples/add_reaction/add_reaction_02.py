import os
from lapsepy.lapse import Lapse

if __name__ == '__main__':
    lapse = Lapse(refresh_token=os.getenv("REFRESH_TOKEN"))

    count = int(input("How many: "))
    msg_id = input("MSG ID: ")
    reaction = input("Reaction: ")

    for _ in range(count):
        lapse.add_reaction(msg_id=msg_id, reaction=reaction)
