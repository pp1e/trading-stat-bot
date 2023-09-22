from datetime import datetime
from database import database
import json


def print_week_statistic():
    data = database.database.fetch_last_week_row()
    user_deposits = database.database.fetch_user_deposits()
    week_profit = json.loads(data[6])
    date_object = datetime.strptime(data[0], "%Y-%m-%d")
    formatted_date = date_object.strftime("%d.%m.%Y")
    total_sum = sum(value for value in user_deposits.values())

    message = f"""
** Данные от {formatted_date} **

**Заработано за неделю:**
+{data[4]}% | +${data[3]}

🔹**Ваня: +${round(week_profit['Ivan92mat'], 2)}**
Депозит: ${user_deposits['Ivan92mat']}
Текущий баланс: ${round(user_deposits['Ivan92mat'] + week_profit['Ivan92mat'], 2)}
Общая прибыль: +${round(user_deposits['Ivan92mat'] + week_profit['Ivan92mat'] - user_deposits['Ivan92mat'], 2)}

🔹**Саня: +${round(week_profit['AlexSkvorz'], 2)}**
Депозит: ${user_deposits['AlexSkvorz']}
Текущий баланс: ${round(user_deposits['AlexSkvorz'] + week_profit['AlexSkvorz'], 2)}
Общая прибыль: +${round(user_deposits['AlexSkvorz'] + week_profit['AlexSkvorz'] - user_deposits['AlexSkvorz'], 2)}

🔹**Ден: +${round(week_profit['p_pie'], 2)}**
Депозит: ${user_deposits['p_pie']}
Текущий баланс: ${round(user_deposits['p_pie'] + week_profit['p_pie'], 2)}
Общая прибыль: +${round(user_deposits['p_pie'] + week_profit['p_pie'] - user_deposits['p_pie'], 2)}

**Всего:** ${total_sum} -> ${data[1]}

[СЛЕДИТЬ](https://fxmonitor.online/u/UQEvKqKD?view=pro)
        """
    return message
