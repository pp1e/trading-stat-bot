from utils import russian_format_today_date


def form_user_balances_info(user_balances):
    today_date = russian_format_today_date()
    message = f"Данные на <b>{today_date}</b>\n\n"

    for user in user_balances.keys():
        message += f"🔹<b>Баланс {user}: ${round(user_balances[user], 2)}</b>\n\n"

    return message
