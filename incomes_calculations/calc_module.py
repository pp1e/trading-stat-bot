import json
from database import database


def calculate_week_statistic():
    user_deposits = database.database.fetch_user_deposits()
    # Обязательно нужно будет переделать логику так, чтобы он за один запрос заполнял в БД строку week_profit.
    # Пока оставлю так. То есть здесь он должен не через следующий запрос данные получать, а из скрэпера.
    # И только потом уже из этой функции передавать все данные целиком в БД
    week_profit = database.database.fetch_week_profit()
    previous_week_balance = database.database.fetch_previous_balance()
    json_previous_week_balance = json.loads(previous_week_balance)

    total_sum = sum(value for value in user_deposits.values())

    for user in user_deposits.keys():
        percent_part_of_deposit = user_deposits[user] * 100 / total_sum

        if user in json_previous_week_balance.keys():
            user_part_of_week_profit = week_profit * percent_part_of_deposit / 100
            json_previous_week_balance[user] += user_part_of_week_profit
        else:
            user_part_of_week_profit = week_profit * percent_part_of_deposit / 100
            json_previous_week_balance[user] = user_deposits[user] + user_part_of_week_profit

    json_new_week_balance = json.dumps(json_previous_week_balance)
    database.database.add_data(json_new_week_balance)
