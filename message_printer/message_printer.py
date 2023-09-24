import datetime


def print_week_statistic(date, week_profit_percets, week_profit, total_profit,
                         user_overall_profits, user_week_profits, user_deposits):
    start_week_date = datetime.datetime.strptime(date, "%Y-%m-%d")
    end_week_date = start_week_date + datetime.timedelta(days=6)
    start_week_date = start_week_date.strftime("%d.%m.%Y")
    end_week_date = end_week_date.strftime("%d.%m.%Y")
    total_sum = sum(value for value in user_deposits.values())

    message = f"""
** Данные за неделю c {start_week_date} по {end_week_date}**

**Заработано за неделю:**
+{week_profit_percets}% | +${week_profit}

🔹**Ваня: +${round(user_week_profits['Ivan92mat'], 2)}**
Депозит: ${user_deposits['Ivan92mat']}
Текущий баланс: ${round(user_deposits['Ivan92mat'] + user_overall_profits['Ivan92mat'], 2)}
Общая прибыль: +${round(user_overall_profits['Ivan92mat'], 2)}

🔹**Саня: +${round(user_week_profits['AlexSkvorz'], 2)}**
Депозит: ${user_deposits['AlexSkvorz']}
Текущий баланс: ${round(user_deposits['AlexSkvorz'] + user_overall_profits['AlexSkvorz'], 2)}
Общая прибыль: +${round(user_overall_profits['AlexSkvorz'], 2)}

🔹**Ден: +${round(user_week_profits['p_pie'], 2)}**
Депозит: ${user_deposits['p_pie']}
Текущий баланс: ${round(user_deposits['p_pie'] + user_overall_profits['p_pie'], 2)}
Общая прибыль: +${round(user_overall_profits['p_pie'], 2)}

**Всего:** ${total_sum} -> ${total_profit}

[СЛЕДИТЬ](https://fxmonitor.online/u/UQEvKqKD?view=pro)
        """
    return message
