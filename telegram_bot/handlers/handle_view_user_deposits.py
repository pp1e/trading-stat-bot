from database import users_rights_table
from telegram_bot.message_generators.user_balances_generator import form_user_balances_info
from telegram_bot.message_generators.welcome_message_generator import send_welcome_message


def handle_view_user_deposits(chat_id, bot, db_connection):
    user_balances = users_rights_table.fetch_user_balances(db_connection)
    message = form_user_balances_info(user_balances)
    bot.send_message(chat_id, message, parse_mode='html')
    send_welcome_message(bot=bot, chat_id=chat_id)
