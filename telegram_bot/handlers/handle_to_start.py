from telegram_bot.message_generators.welcome_message_generator import send_welcome_message
from constants import SELECT_ACTION


def handle_to_start(chat_id, username, user_states, bot):
    user_states[username] = SELECT_ACTION
    send_welcome_message(bot=bot, chat_id=chat_id)

    return user_states
