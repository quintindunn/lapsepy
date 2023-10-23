import os

from lapsepy import Lapse

if __name__ == '__main__':
    lapse = Lapse(os.getenv("REFRESH_TOKEN"))

    # 
    display_name = input("Enter your emojis: ")
    lapse.update_display_name(display_name=display_name)
