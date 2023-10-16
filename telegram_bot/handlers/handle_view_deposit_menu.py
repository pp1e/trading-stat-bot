from telegram_bot.message_generators.deposit_menu_generator import send_user_deposit_menu


def handle_view_deposit_menu(chat_id, bot):
    send_user_deposit_menu(bot=bot, chat_id=chat_id)
