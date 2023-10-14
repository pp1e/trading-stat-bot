import datetime
from num2words import num2words

from telegram_bot.entities.week_stat import WeekStat


def form_week_statistic_message(week_stat: WeekStat):

    rus_start_week_date, rus_end_week_date, rus_week_number = form_data_to_russian_style(
        start_week_date=week_stat.monday_date, week_number=week_stat.week_number
    )

    message = f"<b>{rus_week_number} НЕДЕЛЯ </b> \n\n"
    message += f"Данные за неделю c <b>{rus_start_week_date} по {rus_end_week_date}</b>\n\n"
    message += "Заработано за неделю:\n"
    message += f"<b>+{week_stat.week_profit_percents}% | +${week_stat.week_profit}</b>\n\n"

    for userTag in week_stat.user_week_profits.keys():
        user_balance = week_stat.user_balances[userTag]
        user_overall_profit = week_stat.user_overall_profits[userTag]
        message += f"🔹<b>{userTag}: +${round(week_stat.user_week_profits[userTag], 2)}</b>\n"
        message += f"Текущий баланс: ${round(user_balance, 2)}\n"
        message += f"Общая прибыль: +${round(user_overall_profit, 2)}\n\n"

    message += (f"<b>Всего:</b> ${round(week_stat.overall_balance - week_stat.profit, 2)}"
                f" -> ${round(week_stat.overall_balance, 2)}\n")
    message += f"<b>Прибыль:</b> ${round(week_stat.profit, 2)}\n\n"
    message += '<a href="https://fxmonitor.online/u/UQEvKqKD?view=pro">СЛЕДИТЬ</a>'

    return message


def form_data_to_russian_style(start_week_date, week_number):
    end_week_date = start_week_date + datetime.timedelta(days=6)
    start_week_date = start_week_date.strftime("%d.%m.%Y")
    end_week_date = end_week_date.strftime("%d.%m.%Y")

    week_number = num2words(week_number, to='ordinal', lang='ru').upper()
    week_number = week_number[:-2] + 'АЯ'

    return start_week_date, end_week_date, week_number
