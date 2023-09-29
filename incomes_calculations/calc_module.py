def calculate_week_user_profits(actual_total_sum, user_deposits, user_overall_profits):
    user_week_profits = {}
    previous_total_sum = (sum(value for value in user_deposits.values()) +
                          sum(value for value in user_overall_profits.values()))
    percent = actual_total_sum / previous_total_sum

    for user, deposit in user_deposits.items():
        overall_profit = user_overall_profits.get(user, 0)
        person_deposit_with_profit = deposit + overall_profit
        user_week_profit = (person_deposit_with_profit * percent) - person_deposit_with_profit
        user_overall_profits[user] = overall_profit + user_week_profit
        user_week_profits[user] = user_week_profit

    return user_overall_profits, user_week_profits
