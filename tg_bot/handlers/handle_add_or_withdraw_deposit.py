from database import users_rights_table
from tg_bot.message_generators.simple_messages_generator import send_operation_type_message


def handle_add_or_withdraw_deposit(call, bot, db_connection, operation_type):
    users = users_rights_table.fetch_user_tags(db_connection=db_connection)

    send_operation_type_message(
        operation_type=operation_type,
        bot=bot,
        call=call,
        users=users
    )
