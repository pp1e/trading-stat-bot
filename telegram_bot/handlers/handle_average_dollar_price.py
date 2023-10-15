from telegram_bot.message_generators.average_dollar_price_generator import form_average_dollar_price
from database import deposit_info_table
from telegram_bot.message_generators.welcome_message_generator import send_welcome_message


def handle_average_dollar_price(bot, chat_id, db_connection):
    user_deposits = deposit_info_table.fetch_user_deposits(db_connection=db_connection)

    message = form_average_dollar_price(user_deposits)

    bot.send_message(
        chat_id=chat_id,
        text=message,
        parse_mode='html'
    )

    send_welcome_message(chat_id=chat_id, bot=bot)
