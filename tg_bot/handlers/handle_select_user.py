from constants import WAIT_DEPOSIT, DEPOSIT_ACTION, WITHDRAW_ACTION

from tg_bot.message_generators.simple_messages_generator import send_transaction_amount_question


def handle_select_user(call, bot, user_states, username, operation_type):
    username_pays = call.data.replace('select_user_', '')

    user_states[username] = WAIT_DEPOSIT

    send_transaction_amount_question(
        operation_type=operation_type,
        bot=bot,
        call=call,
        username_pays=username_pays
    )

    return user_states, username_pays
