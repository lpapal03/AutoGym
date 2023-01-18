from datetime import datetime
from datetime import timedelta


def extract_details(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    username = lines[0]
    password = lines[1]
    preference_map = {}
    for i in range(2, len(lines)):
        l = lines[i].split()
        preference_map[l[0]] = l[1]
    return username.replace('\n', ''), password.replace('\n', ''), preference_map


def caluclate_resv_date_and_time(username, preference_map):
    # calculate date to reserve
    today = datetime.now()
    target_date = today + timedelta(days=5)
    resv_date = target_date.strftime("%d-%m-%Y")

    # if target day is Sunday or has no preference then end
    if target_date.weekday() == 6:
        print(username + ' - Target day is Sunday')
        return '', '', True
    if str(target_date.weekday()) not in preference_map.keys():
        print(username + ' - Target day not in preference map')
        return '', '', True
    resv_time = preference_map[str(target_date.weekday())]

    return resv_date, resv_time, False
