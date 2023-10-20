import datetime


def get_current_week_monday():
    today = datetime.date.today()

    return get_monday_by_week_date(today)


def get_last_week_monday():
    return get_current_week_monday() - datetime.timedelta(days=7)


def get_monday_by_week_date(week_date):
    days_since_monday = week_date.weekday()
    monday = week_date - datetime.timedelta(days=days_since_monday)

    return monday


def is_today_weekends():
    today = datetime.date.today()
    day_of_week_day = today.weekday()

    if (day_of_week_day == 5) or (day_of_week_day == 6):
        return True

    return False


def get_string_last_week_monday():
    last_monday = get_current_week_monday() - datetime.timedelta(days=7)
    last_monday = last_monday.strftime("%Y-%m-%d")
    return last_monday


def get_last_week_sunday():
    return get_current_week_monday() - datetime.timedelta(days=1)


def russian_format_today_date():
    today = datetime.date.today()
    today = today.strftime("%d.%m.%Y")

    return today
