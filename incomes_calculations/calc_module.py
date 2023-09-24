def calculate_week_user_profits(week_profit, user_deposits, user_overall_profits):
    user_week_profits = {}

    total_sum = sum(value for value in user_deposits.values())

    for user in user_deposits.keys():
        percent_part_of_deposit = user_deposits[user] * 100 / total_sum
        user_part_of_week_profit = week_profit * percent_part_of_deposit / 100
        user_week_profits[user] = user_part_of_week_profit

        if user in user_overall_profits.keys():
            user_overall_profits[user] += user_part_of_week_profit
        else:
            user_overall_profits[user] = user_part_of_week_profit

    return user_overall_profits, user_week_profits
