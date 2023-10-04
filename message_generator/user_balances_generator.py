import datetime


def form_user_balances_info(user_balances):
    today = datetime.date.today()
    today = today.strftime("%d.%m.%Y")
    message = f"Данные на <b>{today}</b>\n\n"

    for user in user_balances.keys():
        message += f"🔹<b>Баланс {user}: ${round(user_balances[user], 2)}</b>\n\n"

    return message
