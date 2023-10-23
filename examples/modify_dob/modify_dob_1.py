import os

from lapsepy import Lapse

if __name__ == '__main__':
    lapse = Lapse(os.getenv("REFRESH_TOKEN"))

    # DOB: yyyy-mm-dd
    dob = input("Date of birth (yyyy-mm-dd): ")
    lapse.update_dob(dob=dob)
