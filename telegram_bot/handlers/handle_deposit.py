from constants import DEPOSIT_ACTION, WITHDRAW_ACTION, SELECT_ACTION
from database import users_rights_table

from telegram_bot.message_generators.welcome_message_generator import send_welcome_message


def handle_deposit(message, bot, db_connection, username, user_states, unique_user_transaction):
    try:
        deposit_amount = float(message.text)

        if deposit_amount < 0:
            bot.send_message(message.chat.id, "Сумма не может быть отрицательной!")
            return user_states, unique_user_transaction

        save_deposit(
            deposit_amount=deposit_amount,
            chat_id=message.chat.id,
            bot=bot,
            operation_type=unique_user_transaction[username]['operation_type'],
            db_connection=db_connection,
            username_pays=unique_user_transaction[username]['username_pays']
        )

        user_states[username] = SELECT_ACTION
        del unique_user_transaction[username]

        send_welcome_message(bot=bot, chat_id=message.chat.id)

    except ValueError:
        bot.send_message(message.chat.id, "Некорректная сумма. Введите число!")

    return user_states, unique_user_transaction


def save_deposit(deposit_amount, chat_id, bot, operation_type, db_connection, username_pays):
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
