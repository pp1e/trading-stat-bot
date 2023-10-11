from database import users_rights_table
from tg_bot.message_generators.simple_messages_generator import send_operation_type_message
from constants import DEPOSIT_ACTION


def handle_add_or_withdraw_deposit(call, bot, db_connection, operation_type):
    users = users_rights_table.fetch_user_tags(db_connection=db_connection)

    if operation_type == DEPOSIT_ACTION:
        message = 'Кто пополнил баланс'
    else:
        message = 'Кто снял деньги?'

    send_operation_type_message(
        bot=bot,
        chat_id=call.message.chat.id,
        users=users,
        message=message
    )
