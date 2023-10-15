import datetime


def form_average_dollar_price(user_deposits):
    today = datetime.date.today()
    today = today.strftime("%d.%m.%Y")
    message = f"Данные на <b>{today}</b>\n\n"

    for user in user_deposits:
        message += (f"🔹<b>Средняя цена закупки доллара {user[0]}: "
                    f"{round(user[1]/user[2], 2)}₽</b>\n\n")

    return message
