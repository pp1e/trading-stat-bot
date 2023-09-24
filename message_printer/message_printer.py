import datetime


def print_week_statistic(date, week_profit_percets, week_profit, total_profit,
                         user_overall_profits, user_week_profits, user_deposits):
    start_week_date = datetime.datetime.strptime(date, "%Y-%m-%d")
    end_week_date = start_week_date + datetime.timedelta(days=6)
    start_week_date = start_week_date.strftime("%d.%m.%Y")
    end_week_date = end_week_date.strftime("%d.%m.%Y")
    total_sum = sum(value for value in user_deposits.values())

    message = f"Данные за неделю c <b>{start_week_date} по {end_week_date}</b>\n\n"
    message += "Заработано за неделю:\n"
    message += f"<b>+{week_profit_percets}% | +${week_profit}</b>\n\n"

    for userTag in user_week_profits.keys():
        message += f"🔹<b>{userTag}: +${round(user_week_profits[userTag], 2)}</b>\n"
        message += f"Депозит: ${user_deposits[userTag]}\n"
        message += f"Текущий баланс: ${round(user_deposits[userTag] + user_overall_profits[userTag], 2)}\n"
        message += f"Общая прибыль: +${round(user_overall_profits[userTag], 2)}\n\n"

    message += f"<b>Всего:</b> ${total_sum} -> ${total_profit}\n\n"
    message += '<a href="https://fxmonitor.online/u/UQEvKqKD?view=pro">СЛЕДИТЬ</a>'

    return message
