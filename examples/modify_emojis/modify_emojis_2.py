import os

from lapsepy import Lapse

if __name__ == '__main__':
    lapse = Lapse(os.getenv("REFRESH_TOKEN"))

    emojis = []
    for _ in range(5):
        if (a := input("Emojis: ")) != "":
            emojis.append(a)
        else:
            break

    lapse.update_emojis(emojis)
