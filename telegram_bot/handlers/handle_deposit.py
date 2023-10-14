from constants import DEPOSIT_ACTION, WITHDRAW_ACTION, SELECT_ACTION
from database import users_rights_table

from telegram_bot.message_generators.welcome_message_generator import send_welcome_message


def handle_deposit(message, bot, db_connection, username, user_states, username_pays, operation_type):
    try:
        deposit_amount = float(message.text)

        handle_deposit_amount(
            deposit_amount=deposit_amount,
            chat_id=message.chat.id,
            bot=bot,
            operation_type=operation_type,
            db_connection=db_connection,
            username_pays=username_pays
        )

        user_states[username] = SELECT_ACTION

        send_welcome_message(bot=bot, chat_id=message.chat.id)

    except ValueError:
        bot.send_message(message.chat.id, "Некорректная сумма. Введите число!")

    return user_states


def handle_deposit_amount(deposit_amount, chat_id, bot, operation_type, db_connection, username_pays):
    if deposit_amount >= 0:

        if operation_type == DEPOSIT_ACTION:
            bot.send_message(chat_id, f"Пользователь {username_pays} "
                                              f"внес {deposit_amount}USD")

            users_rights_table.update_balance(
                db_connection=db_connection,
                username_pays=username_pays,
                amount=deposit_amount
            )
        elif operation_type == WITHDRAW_ACTION:
            bot.send_message(chat_id, f"Пользователь {username_pays} "
                                              f"снял {deposit_amount}USD")

            users_rights_table.update_balance(
                db_connection=db_connection,
                username_pays=username_pays,
                amount=-deposit_amount
            )

    else:
        bot.send_message(chat_id, "Сумма не может быть отрицательной!")
