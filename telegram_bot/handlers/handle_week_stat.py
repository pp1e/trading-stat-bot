import json
from datetime import datetime

import utils
from config.storage_config import STORAGE_CONFIG
from telegram_bot.message_generators import week_statistic_generator
from telegram_bot.entities.week_stat import WeekStat
from database import users_rights_table
from database import weeks_stats_table


def handle_view_last_statistic(chat_id, bot, db_connection):
    week_stat = get_week_statistic(db_connection)
    message = week_statistic_generator.form_week_statistic_message(week_stat, add_balances=True)

    bot.send_photo(
        chat_id=chat_id,
        photo=week_stat.screenshot,
        caption=message,
        parse_mode='html',
    )


def handle_view_specified_statistic(chat_id, bot, db_connection, week_date):
    week_stat = get_week_statistic(db_connection, week_date)
    if week_stat is None:
        bot.send_message(
            chat_id=chat_id,
            text="За эту неделю нету статистики 😞"
        )
        return

    message = week_statistic_generator.form_week_statistic_message(week_stat)
    bot.send_photo(
        chat_id=chat_id,
        photo=week_stat.screenshot,
        caption=message,
        parse_mode='html',
    )


def get_week_statistic(db_connection, week_date=None):
    if week_date:
        week_monday = utils.get_monday_by_week_date(week_date)
        week_data = weeks_stats_table.fetch_week_stat(db_connection, week_monday)
    else:
        week_data = get_latest_week_data(db_connection)
        week_monday = datetime.fromisoformat(week_data[0]).date()

    if week_data is None:
        return None

    user_balances = users_rights_table.fetch_user_balances(db_connection)
    week_number = weeks_stats_table.fetch_week_number(db_connection, week_monday)

    return WeekStat(
        monday_date=week_monday,
        week_profit=week_data[3],
        week_profit_percents=week_data[5],
        overall_balance=week_data[1],
        profit=week_data[2],
        profit_percents=week_data[4],
        user_overall_profits=json.loads(week_data[6]),
        user_week_profits=json.loads(week_data[7]),
        user_balances=user_balances,
        screenshot=load_screenshot(week_monday),
        week_number=week_number
    )


def get_latest_week_data(db_connection):
    current_week_monday = utils.get_current_week_monday()
    data = weeks_stats_table.fetch_week_stat(db_connection, current_week_monday)

    if data is None:
        last_week_monday = utils.get_last_week_monday()
        data = weeks_stats_table.fetch_week_stat(db_connection, last_week_monday)

    return data


def load_screenshot(screen_date):
    return open(f'{STORAGE_CONFIG["path_to_screens"]}/{screen_date}.png', 'rb')
