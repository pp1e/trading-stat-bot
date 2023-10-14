from constants import SELECT_ACTION
from telegram_bot.message_generators.welcome_message_generator import send_welcome_message
from database import users_rights_table


def handle_start_command(message, bot, db_connection, user_states):
    username = message.from_user.username
    user_states[username] = SELECT_ACTION

    users_rights_table.add_new_user(db_connection=db_connection, username=username)

    send_welcome_message(bot=bot, chat_id=message.chat.id)

    return username, user_states
