def calculate_week_user_profits(actual_overall_balance, last_week_user_balances, last_week_user_overall_profits):
    user_current_week_profits = {}
    user_overall_profits = {}

    last_week_overall_balance = sum(value for value in last_week_user_balances.values())
    percent = actual_overall_balance / last_week_overall_balance

    for user_tag, user_balance in last_week_user_balances.items():
        last_week_user_overall_profit = last_week_user_overall_profits.get(user_tag, 0)
        user_current_week_profit = (user_balance * percent) - user_balance
        user_overall_profits[user_tag] = last_week_user_overall_profit + user_current_week_profit
        user_current_week_profits[user_tag] = user_current_week_profit

    return user_overall_profits, user_current_week_profits
