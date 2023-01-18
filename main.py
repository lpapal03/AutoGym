import os
import sys
import time
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
    print("Cycle done")


if __name__ == "__main__":
    if sys.argv.__contains__('hl'):
        HEADLESS = True

    if len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv.__contains__('hl')):
        reserve_for_all()
        exit(0)
    
    if sys.argv.__contains__('s'):
        schedule.every().day.at("08:01").do(reserve_for_all)
        print('Scheduled')
        while True:
            schedule.run_pending()
            time.sleep(1)    

