from constants import DEPOSIT_ACTION, WITHDRAW_ACTION, SELECT_ACTION, WAIT_RUBLE_DEPOSIT
from database import users_rights_table, deposit_info_table
from utils import russian_format_today_date

from telegram_bot.message_generators.welcome_message_generator import send_welcome_message


def handle_dollar_deposit(message, bot, db_connection, username, user_states, unique_user_transaction):
    try:
        dollar_deposit_amount = float(message.text)

        if dollar_deposit_amount <= 0:
            bot.send_message(message.chat.id, "Сумма не может быть отрицательной!")
            return user_states, unique_user_transaction

        save_dollar_deposit(
            dollar_deposit_amount=dollar_deposit_amount,
            chat_id=message.chat.id,
            bot=bot,
            operation_type=unique_user_transaction[username]['operation_type'],
            db_connection=db_connection,
            username_pays=unique_user_transaction[username]['username_pays']
        )

        bot.send_message(message.chat.id, 'Какая сумма операции в рублях?')

        if unique_user_transaction[username]['operation_type'] == DEPOSIT_ACTION:
            user_states[username] = WAIT_RUBLE_DEPOSIT
            unique_user_transaction[username]['dollar_deposit_amount'] = dollar_deposit_amount
        else:
            user_states[username] = SELECT_ACTION
            del unique_user_transaction[username]
            send_welcome_message(bot=bot, chat_id=message.chat.id)

        return user_states, unique_user_transaction

    except ValueError:
        bot.send_message(message.chat.id, "Некорректная сумма. Введите число!")
        return user_states, unique_user_transaction


def save_dollar_deposit(dollar_deposit_amount, chat_id, bot, operation_type, db_connection, username_pays):
    if operation_type == DEPOSIT_ACTION:
        bot.send_message(chat_id, f"{username_pays} внес {dollar_deposit_amount}$")

        users_rights_table.update_balance(
            db_connection=db_connection,
            username_pays=username_pays,
            amount=dollar_deposit_amount
        )

    elif operation_type == WITHDRAW_ACTION:
        bot.send_message(chat_id, f"{username_pays} снял {dollar_deposit_amount}$")

        users_rights_table.update_balance(
            db_connection=db_connection,
            username_pays=username_pays,
            amount=-dollar_deposit_amount
        )


def handle_ruble_deposit(message, bot, db_connection, username, user_states, unique_user_transaction):
    try:
        ruble_deposit_amount = float(message.text)

        if ruble_deposit_amount <= 0:
            bot.send_message(message.chat.id, "Сумма не может быть отрицательной!")
            return user_states, unique_user_transaction

        save_ruble_deposit(
            ruble_deposit_amount=ruble_deposit_amount,
            dollar_deposit_amount=unique_user_transaction[username]['dollar_deposit_amount'],
            bot=bot,
            chat_id=message.chat.id,
            username_pays=unique_user_transaction[username]['username_pays'],
            db_connection=db_connection
        )

        user_states[username] = SELECT_ACTION
        del unique_user_transaction[username]

        send_welcome_message(bot=bot, chat_id=message.chat.id)

        return user_states, unique_user_transaction

    except ValueError:
        bot.send_message(message.chat.id, "Некорректная сумма. Введите число!")
        return user_states, unique_user_transaction


def save_ruble_deposit(ruble_deposit_amount, dollar_deposit_amount, bot, chat_id, username_pays, db_connection):
    bot.send_message(chat_id, f'{username_pays} внес {ruble_deposit_amount}₽')

    max_id, today_date = form_data_to_save(db_connection=db_connection)
    dollar_price = ruble_deposit_amount / dollar_deposit_amount

    deposit_info_table.insert_deposit(
        db_connection=db_connection,
        id=max_id,
        telegram_tag=username_pays,
        date=today_date,
        user_rubles_deposit=ruble_deposit_amount,
        dollar_price=dollar_price,
        dollar_amount=dollar_deposit_amount
    )

    bot.send_message(chat_id, f'{username_pays} внес {dollar_deposit_amount}$, по цене {dollar_price}₽ '
                              f'на сумму {ruble_deposit_amount}₽')


def form_data_to_save(db_connection):
    max_id = deposit_info_table.fetch_max_id(db_connection)

    if max_id is None:
        max_id = 1
    else:
        max_id = max_id[0] + 1

    today_date = russian_format_today_date()
    return max_id, today_date
