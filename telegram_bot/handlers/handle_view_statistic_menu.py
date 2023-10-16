from telegram_bot.message_generators.statistic_menu_generator import send_user_statistic_menu


def handle_view_statistic_menu(chat_id, bot):
    send_user_statistic_menu(bot=bot, chat_id=chat_id)
