from utils import russian_format_today_date


def form_deposit_statistic(user_deposits, user_balances):
    today_date = russian_format_today_date()
    overall_balance = sum(user_balances.values())
    message = f"Данные на <b>{today_date}</b>\n\n"

    for username in user_balances.keys():
        try:
            message += f"🔹Пользователь <b>{username}</b>\n\n"
            message += f"Текущий баланс: <b>${round(user_balances[username], 2)}</b>\n"
            message += (f"Средняя цена закупки доллара: <b>₽"
                        f"{round(user_deposits[username]['rubles'] / user_deposits[username]['dollars'], 2)}</b>\n")
            message += (f"Процент от всего баланса: <b>"
                        f"{round(user_balances[username] / overall_balance * 100, 2)}%</b>\n\n")
        except KeyError:
            continue

    return message
