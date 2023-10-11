from constants import DEPOSIT_ACTION, WITHDRAW_ACTION, SELECT_ACTION
from database import users_rights_table

from tg_bot.message_generators.welcome_message_generator import send_welcome_message
from tg_bot.message_generators.simple_messages_generator import send_operation_result_message


def handle_deposit(message, bot, db_connection, username, user_states, username_pays, operation_type):
    try:
        deposit_amount = float(message.text)

        handle_deposit_amount(
            deposit_amount=deposit_amount,
            message=message,
            bot=bot,
            operation_type=operation_type,
            db_connection=db_connection,
            username_pays=username_pays
        )

        user_states[username] = SELECT_ACTION

        send_welcome_message(bot, message)
    except ValueError:
        bot.send_message(message.chat.id, "Некорректная сумма. Введите число!")

    return user_states


def handle_deposit_amount(deposit_amount, message, bot, operation_type, db_connection, username_pays):
    if deposit_amount >= 0:

        send_operation_result_message(
            operation_type=operation_type,
            bot=bot,
            message=message,
            username_pays=username_pays,
            deposit_amount=deposit_amount
        )

        if operation_type == DEPOSIT_ACTION:
            users_rights_table.update_balance(db_connection, username_pays, deposit_amount)
        elif operation_type == WITHDRAW_ACTION:
            users_rights_table.update_balance(db_connection, username_pays, -deposit_amount)

    else:
        bot.send_message(message.chat.id, "Сумма не может быть отрицательной!")
