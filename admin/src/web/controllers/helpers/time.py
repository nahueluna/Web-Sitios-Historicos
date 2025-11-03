from datetime import datetime


def date_is_greater_than(date1, date2):
    date1_millis = int(datetime.strptime(date1, "%Y-%m-%d").timestamp())
    date2_millis = int(datetime.strptime(date2, "%Y-%m-%d").timestamp())

    return date1_millis > date2_millis