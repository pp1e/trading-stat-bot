from telegram_bot.message_generators.welcome_message_generator import send_welcome_message
from constants import SELECT_ACTION


def handle_to_start(chat_id, username, user_states, bot, unique_user_transaction):
    user_states[username] = SELECT_ACTION

    if username in unique_user_transaction.keys():
        del unique_user_transaction[username]

    send_welcome_message(bot=bot, chat_id=chat_id)

    return user_states, unique_user_transaction
