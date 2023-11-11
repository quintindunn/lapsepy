import os

from lapsepy import Lapse

if __name__ == '__main__':
    lapse = Lapse(os.getenv("REFRESH_TOKEN"))

    user = input("User: ")
    result = lapse.search_for_user(user, first=1)
    print(result)
