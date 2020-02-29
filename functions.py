from datetime import datetime


def get_today():
    now = datetime.today()
    today = datetime(now.year, now.month, now.day)

    return today
