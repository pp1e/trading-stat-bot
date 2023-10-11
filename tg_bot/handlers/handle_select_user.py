from constants import WAIT_DEPOSIT, DEPOSIT_ACTION, WITHDRAW_ACTION


def handle_select_user(call, bot, user_states, username, operation_type):
    username_pays = call.data.replace('select_user_', '')

    user_states[username] = WAIT_DEPOSIT

    if operation_type == DEPOSIT_ACTION:
        bot.send_message(call.message.chat.id, f"На сколько пополнил {username_pays}?")
    elif operation_type == WITHDRAW_ACTION:
        bot.send_message(call.message.chat.id, f"Сколько снял {username_pays}?")

    return user_states, username_pays
