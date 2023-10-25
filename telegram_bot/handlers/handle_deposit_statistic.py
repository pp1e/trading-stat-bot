from telegram_bot.message_generators.deposit_statistic_generator import form_deposit_statistic
from database import deposit_info_table, users_rights_table
from telegram_bot.message_generators.welcome_message_generator import send_welcome_message
import utils


def handle_deposit_statistic(bot, chat_id, db_connection):
    user_deposits = utils.parse_user_deposits_to_dict(
        query_result=deposit_info_table.fetch_user_deposits(db_connection=db_connection))
    user_balances = utils.parse_user_balances_to_dict(
        query_result=users_rights_table.fetch_user_balances(db_connection=db_connection))

    message = form_deposit_statistic(user_deposits=user_deposits, user_balances=user_balances)

    bot.send_message(
        chat_id=chat_id,
        text=message,
        parse_mode='html'
    )

    send_welcome_message(chat_id=chat_id, bot=bot)
