import os
import sys
import time
from datetime import datetime
from datetime import timedelta

import schedule as schedule
import reserver
import tools

DEBUG = True
HEADLESS = False


def reserve_for_all():
    # iterate files in /users and extract info for each and run reserver on them
    for file in os.listdir("users"):
        try:
            username, password, preference_map = tools.extract_details('users/' + file)
            r_date, r_time, err = tools.caluclate_resv_date_and_time(username, preference_map)
            if not err:
                reserver.reserve_gym_spot(username, password, r_date, r_time, HEADLESS, DEBUG)
        except Exception:
            print('Error with', file)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        reserve_for_all()
    elif len(sys.argv) > 1 and sys.argv[1] == 's':
        schedule.every().day.at("08:01").do(reserve_for_all)
        while True:
            schedule.run_pending()
            time.sleep(1)
