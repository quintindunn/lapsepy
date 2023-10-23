import os

from lapsepy import Lapse

if __name__ == '__main__':
    lapse = Lapse(os.getenv("REFRESH_TOKEN"))

    username = input("New Display Name: ")
    lapse.update_username(username=username)
