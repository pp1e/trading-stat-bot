from constants import WAIT_DEPOSIT, DEPOSIT_ACTION, WITHDRAW_ACTION


def handle_select_user(call, bot, user_states, username, unique_user_transaction):
    username_pays = call.data.replace('select_user_', '')

    user_states[username] = WAIT_DEPOSIT
    unique_user_transaction['username_pays'] = username_pays

    if unique_user_transaction['operation_type'] == DEPOSIT_ACTION:
        bot.send_message(call.message.chat.id, f"На сколько пополнил {username_pays}?")
    elif unique_user_transaction['operation_type'] == WITHDRAW_ACTION:
        bot.send_message(call.message.chat.id, f"Сколько снял {username_pays}?")

    return unique_user_transaction
