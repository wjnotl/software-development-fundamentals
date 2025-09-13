from datetime import datetime
from dateutil.relativedelta import relativedelta


def add_date_delta(date, addType, number):
    return date + relativedelta(**{addType: number})


def get_datetime_from_string(date_str=None, time_str=None):
    if date_str and time_str:
        return datetime.strptime(date_str + " " + time_str, "%Y-%m-%d %I:%M:%p")
    elif date_str:
        return datetime.strptime(date_str, "%Y-%m-%d")
    else:
        return datetime.strptime(time_str, "%I:%M:%p")


def get_time_from_string(hour, minute, meridiem):
    return datetime.strptime(hour + ":" + minute + ":" + meridiem, "%I:%M:%p")


def is_datetime_expired(date, time):
    now = datetime.now()
    currentDatetime = get_datetime_from_string(date, time)

    return currentDatetime < now
