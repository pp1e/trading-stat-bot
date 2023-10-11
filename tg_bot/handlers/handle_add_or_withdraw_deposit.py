from constants import BOT_COMMANDS
from database import users_rights_table
from tg_bot.handlers.create_buttons import create_buttons
from tg_bot.message_generators.simple_messages_generator import send_operation_type_message


def handle_add_or_withdraw_deposit(call, bot, db_connection, operation_type):
    users = users_rights_table.fetch_user_tags(db_connection)

    button_parameters = {name: f'select_user_{name}' for name in users}

    button_parameters['Вернуться назад'] = BOT_COMMANDS['COMMAND_TO_START']

    markup = create_buttons(button_parameters)

    send_operation_type_message(
        operation_type=operation_type,
        bot=bot,
        call=call,
        markup=markup
    )
