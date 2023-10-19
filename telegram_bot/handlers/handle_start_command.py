from constants import SELECT_ACTION
from telegram_bot.message_generators.welcome_message_generator import send_welcome_message


def handle_start_command(message, bot, user_states):
    username = message.from_user.username
    user_states[username] = SELECT_ACTION

    send_welcome_message(bot=bot, chat_id=message.chat.id)

    return user_states
