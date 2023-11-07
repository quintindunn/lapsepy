import os
from datetime import datetime

from lapsepy import Lapse

if __name__ == '__main__':
    lapse = Lapse(os.getenv("REFRESH_TOKEN"))

    # DOB: yyyy-mm-dd
    dob = input("Date of birth (yyyy-mm-dd): ")
    try:
        dob_date = datetime.strptime(dob, "%Y-%m-%d")
    except ValueError:
        exit("Invalid date format. Please use yyyy-mm-dd format.")

    lapse.update_dob(dob_date)