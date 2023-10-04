import datetime


def formation_of_week_statistic(date, week_profit_percents, week_profit, overall_balance, overall_profit,
                                user_overall_profits, user_week_profits, user_balances):
    start_week_date = datetime.datetime.strptime(date, "%Y-%m-%d")
    end_week_date = start_week_date + datetime.timedelta(days=6)
    start_week_date = start_week_date.strftime("%d.%m.%Y")
    end_week_date = end_week_date.strftime("%d.%m.%Y")

    message = f"Данные за неделю c <b>{start_week_date} по {end_week_date}</b>\n\n"
    message += "Заработано за неделю:\n"
    message += f"<b>+{week_profit_percents}% | +${week_profit}</b>\n\n"

    for userTag in user_week_profits.keys():
        user_balance = user_balances[userTag]
        user_overall_profit = user_overall_profits[userTag]
        message += f"🔹<b>{userTag}: +${round(user_week_profits[userTag], 2)}</b>\n"
        message += f"Депозит: ${round(user_balance - user_overall_profit)}\n"
        # TODO нужно ли здесь вообще показывать депозит???
        message += f"Текущий баланс: ${round(user_balance, 2)}\n"
        message += f"Общая прибыль: +${round(user_overall_profit, 2)}\n\n"

    message += f"<b>Всего:</b> ${round(overall_balance - overall_profit, 2)} -> ${round(overall_balance, 2)}\n"
    message += f"<b>Прибыль:</b> ${round(overall_profit, 2)}\n\n"
    message += '<a href="https://fxmonitor.online/u/UQEvKqKD?view=pro">СЛЕДИТЬ</a>'

    return message
