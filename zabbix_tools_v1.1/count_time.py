import datetime
import time


def count_today_start_time():
    now = datetime.datetime.now()
    now1 = str(now).split(".", 1)[0]
    now2 = now1.split(" ", 1)[1]
    now3 = now2.split(":", 2)
    hour, minu, sec = now3
    today_lost_secondes = int(hour) * 60 * 60 + int(minu) * 60 + int(sec)
    now_time = int(str(time.time()).split(".", 1)[0])
    today_start_time = now_time - today_lost_secondes
    return today_start_time, now_time


def count_lost_n_hour(lost_n_hour):
    end_time = int(str(time.time()).split(".", 1)[0])
    start_time = end_time - lost_n_hour * 60 * 60
    return start_time, end_time