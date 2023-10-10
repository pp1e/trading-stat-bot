from tg_bot.message_generators.welcome_message_generator import send_welcome_message
from constants import SELECT_ACTION


def handle_to_start(call, username, user_states, bot):
    user_states[username] = SELECT_ACTION
    send_welcome_message(bot, call.message)

    return user_states
