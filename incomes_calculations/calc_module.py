import json
from database import database


def calculate_week_user_profits(week_profit):
    user_deposits = database.database.fetch_user_deposits()
    previous_week_balance = database.database.fetch_previous_balance()
    previous_week_balance = json.loads(previous_week_balance)

    total_sum = sum(value for value in user_deposits.values())

    for user in user_deposits.keys():
        percent_part_of_deposit = user_deposits[user] * 100 / total_sum

        if user in previous_week_balance.keys():
            user_part_of_week_profit = week_profit * percent_part_of_deposit / 100
            previous_week_balance[user] += user_part_of_week_profit
        else:
            user_part_of_week_profit = week_profit * percent_part_of_deposit / 100
            previous_week_balance[user] = user_deposits[user] + user_part_of_week_profit

    json_current_week_balance = json.dumps(previous_week_balance)

    return json_current_week_balance
