from database import users_rights_table
from tg_bot.message_generators.user_balances_generator import form_user_balances_info
from tg_bot.message_generators.welcome_message_generator import send_welcome_message


def handle_view_user_deposits(call, bot, db_connection):
    user_balances = users_rights_table.fetch_user_balances(db_connection)
    message = form_user_balances_info(user_balances)
    bot.send_message(call.message.chat.id, message, parse_mode='html')
    send_welcome_message(bot, call.message)
