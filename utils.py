import datetime


def get_current_week_monday():
    today = datetime.date.today()
    days_since_monday = today.weekday()
    monday = today - datetime.timedelta(days=days_since_monday)

    return monday


def get_last_week_monday():
    return get_current_week_monday() - datetime.timedelta(days=7)


def is_today_weekends():
    today = datetime.date.today()
    day_of_week_day = today.weekday()

    if (day_of_week_day == 5) or (day_of_week_day == 6):
        return True

    return False
