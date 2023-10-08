def calculate_week_user_profits(actual_overall_balance, last_week_overall_balance,
                                user_balances, last_week_user_overall_profits):
    user_current_week_profits = {}
    user_overall_profits = {}

    last_week_overall_balance = check_correct_last_week_overall_balance(last_week_overall_balance, user_balances)
    percent = actual_overall_balance / last_week_overall_balance

    for user_tag, user_balance in user_balances.items():
        last_week_user_overall_profit = last_week_user_overall_profits.get(user_tag, 0)
        user_current_week_profit = (user_balance * percent) - user_balance
        user_overall_profits[user_tag] = last_week_user_overall_profit + user_current_week_profit
        user_current_week_profits[user_tag] = user_current_week_profit

    return user_overall_profits, user_current_week_profits


def check_correct_last_week_overall_balance(last_week_overall_balance, user_balances):
    total_sum = sum(value for value in user_balances.values())

    if total_sum != last_week_overall_balance:
        last_week_overall_balance += total_sum - last_week_overall_balance

    return last_week_overall_balance
