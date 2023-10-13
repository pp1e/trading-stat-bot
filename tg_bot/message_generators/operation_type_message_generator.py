from constants import BOT_COMMANDS
from tg_bot.message_generators.create_buttons import create_buttons


def send_operation_type_message(bot, chat_id, users, message):
    button_parameters = {name: f'select_user_{name}' for name in users}

    button_parameters['Вернуться назад'] = BOT_COMMANDS['COMMAND_TO_START']

    markup = create_buttons(button_parameters=button_parameters)

    bot.send_message(chat_id, message, reply_markup=markup)
