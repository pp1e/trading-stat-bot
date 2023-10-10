from constants import DEPOSIT_ACTION, BOT_COMMANDS
from database import users_rights_table
from tg_bot.handlers.handle_create_buttons import create_buttons


def handle_add_or_withdraw_deposit(call, bot, db_connection, operation_type):
    users = users_rights_table.fetch_user_tags(db_connection)

    button_parameters = {name: f'select_user_{name}' for name in users}

    button_parameters['Вернуться назад'] = BOT_COMMANDS['COMMAND_TO_START']

    markup = create_buttons(button_parameters)

    if operation_type == DEPOSIT_ACTION:
        bot.send_message(call.message.chat.id, 'Кто пополнил балик?', reply_markup=markup)
    else:
        bot.send_message(call.message.chat.id, 'Кто снял деньги?', reply_markup=markup)
