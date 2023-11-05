import os
from lapsepy.lapse import Lapse

if __name__ == '__main__':
    lapse = Lapse(refresh_token=os.getenv("REFRESH_TOKEN"))

    # Develop in 15 seconds
    msg_id = input("MSG ID: ")
    reaction = input("Reaction: ")
    # Get friend object
    friend = lapse.add_reaction(msg_id=msg_id, reaction=reaction)
