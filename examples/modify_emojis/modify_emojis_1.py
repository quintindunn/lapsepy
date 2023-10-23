import os

from lapsepy import Lapse

if __name__ == '__main__':
    lapse = Lapse(os.getenv("REFRESH_TOKEN"))

    emojis = list(input("Emojis: "))
    lapse.update_emojis(emojis=emojis)
