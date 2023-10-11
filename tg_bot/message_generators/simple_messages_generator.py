from constants import BOT_COMMANDS
from tg_bot.message_generators.create_buttons import create_buttons


def send_operation_type_message(bot, chat_id, users, message):
    button_parameters = {name: f'select_user_{name}' for name in users}

    button_parameters['Вернуться назад'] = BOT_COMMANDS['COMMAND_TO_START']

    markup = create_buttons(button_parameters=button_parameters)

    bot.send_message(chat_id, message, reply_markup=markup)


def send_user_rights(bot, chat_id):
    markup = create_buttons(
        button_parameters={
            'Пополнить баланс': BOT_COMMANDS['COMMAND_ADD_DEPOSIT'],
            'Снять деньги': BOT_COMMANDS['COMMAND_WITHDRAW_MONEY'],
            'Посмотреть информацию о балансах': BOT_COMMANDS['COMMAND_VIEW_USER_DEPOSITS'],
            'Вернуться назад': BOT_COMMANDS['COMMAND_TO_START']
        }
    )

    bot.send_message(chat_id, 'Я могу выполнить эти функции', reply_markup=markup)
