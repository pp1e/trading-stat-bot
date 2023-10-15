from telegram_bot.message_generators.user_rights_message_generator import send_user_rights


def handle_interact_with_deposit(chat_id, bot):
    send_user_rights(bot=bot, chat_id=chat_id)
