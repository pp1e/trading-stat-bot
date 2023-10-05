import datetime
from num2words import num2words


def form_week_statistic(date, week_profit_percents, week_profit, overall_balance, overall_profit,
                        user_overall_profits, user_week_profits, user_balances, number_of_week):

    rus_start_week_date, rus_end_week_date, rus_number_of_week = form_data_to_russian_style(date, number_of_week)

    message = f"<b>{rus_number_of_week} НЕДЕЛЯ </b> \n\n"
    message += f"Данные за неделю c <b>{rus_start_week_date} по {rus_end_week_date}</b>\n\n"
    message += "Заработано за неделю:\n"
    message += f"<b>+{week_profit_percents}% | +${week_profit}</b>\n\n"

    for userTag in user_week_profits.keys():
        user_balance = user_balances[userTag]
        user_overall_profit = user_overall_profits[userTag]
        message += f"🔹<b>{userTag}: +${round(user_week_profits[userTag], 2)}</b>\n"
        message += f"Текущий баланс: ${round(user_balance, 2)}\n"
        message += f"Общая прибыль: +${round(user_overall_profit, 2)}\n\n"

    message += f"<b>Всего:</b> ${round(overall_balance - overall_profit, 2)} -> ${round(overall_balance, 2)}\n"
    message += f"<b>Прибыль:</b> ${round(overall_profit, 2)}\n\n"
    message += '<a href="https://fxmonitor.online/u/UQEvKqKD?view=pro">СЛЕДИТЬ</a>'

    return message


def form_data_to_russian_style(date, number_of_week):
    start_week_date = datetime.datetime.strptime(date, "%Y-%m-%d")
    end_week_date = start_week_date + datetime.timedelta(days=6)
    start_week_date = start_week_date.strftime("%d.%m.%Y")
    end_week_date = end_week_date.strftime("%d.%m.%Y")

    number_of_week = num2words(number_of_week, to='ordinal', lang='ru').upper()
    female_number_of_week = number_of_week[:-2] + 'АЯ'

    return start_week_date, end_week_date, female_number_of_week
