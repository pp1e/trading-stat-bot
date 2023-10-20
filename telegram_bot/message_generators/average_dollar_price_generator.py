from utils import russian_format_today_date


def form_average_dollar_price(user_deposits):
    today_date = russian_format_today_date()
    message = f"Данные на <b>{today_date}</b>\n\n"

    for user in user_deposits:
        message += (f"🔹<b>Средняя цена закупки доллара {user[0]}: "
                    f"{round(user[1] / user[2], 2)}₽</b>\n\n")

    return message
