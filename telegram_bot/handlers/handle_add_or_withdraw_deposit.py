from database import users_rights_table
from telegram_bot.message_generators.operation_type_message_generator import send_operation_type_message
from constants import DEPOSIT_ACTION


def handle_add_or_withdraw_deposit(chat_id, bot, db_connection, operation_type):
    users = users_rights_table.fetch_user_tags(db_connection=db_connection)

    if operation_type == DEPOSIT_ACTION:
        message = 'Кто пополнил баланс?'
    else:
        message = 'Кто снял деньги?'

    send_operation_type_message(
        bot=bot,
        chat_id=chat_id,
        users=users,
        message=message
    )
