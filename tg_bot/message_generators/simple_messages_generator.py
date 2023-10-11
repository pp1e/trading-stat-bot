from constants import DEPOSIT_ACTION, WITHDRAW_ACTION, BOT_COMMANDS
from tg_bot.message_generators.create_buttons import create_buttons


def send_operation_type_message(operation_type, bot, call, users):
    button_parameters = {name: f'select_user_{name}' for name in users}

    button_parameters['Вернуться назад'] = BOT_COMMANDS['COMMAND_TO_START']

    markup = create_buttons(button_parameters=button_parameters)

    if operation_type == DEPOSIT_ACTION:
        bot.send_message(call.message.chat.id, 'Кто пополнил баланс?', reply_markup=markup)
    else:
        bot.send_message(call.message.chat.id, 'Кто снял деньги?', reply_markup=markup)


def send_operation_result_message(operation_type, bot, message, username_pays, deposit_amount):
    if operation_type == DEPOSIT_ACTION:
        bot.send_message(message.chat.id, f"Пользователь {username_pays} "
                                          f"внес {deposit_amount}USD")
    elif operation_type == WITHDRAW_ACTION:
        bot.send_message(message.chat.id, f"Пользователь {username_pays} "
                                          f"снял {deposit_amount}USD")


def send_user_rights(bot, call):
    markup = create_buttons(
        button_parameters={
            'Пополнить баланс': BOT_COMMANDS['COMMAND_ADD_DEPOSIT'],
            'Снять деньги': BOT_COMMANDS['COMMAND_WITHDRAW_MONEY'],
            'Посмотреть информацию о балансах': BOT_COMMANDS['COMMAND_VIEW_USER_DEPOSITS'],
            'Вернуться назад': BOT_COMMANDS['COMMAND_TO_START']
        }
    )

    bot.send_message(call.message.chat.id, 'Я могу выполнить эти функции', reply_markup=markup)


def send_transaction_amount_question(operation_type, bot, call, username_pays):
    if operation_type == DEPOSIT_ACTION:
        bot.send_message(call.message.chat.id, f"На сколько пополнил {username_pays}?")
    elif operation_type == WITHDRAW_ACTION:
        bot.send_message(call.message.chat.id, f"Сколько снял {username_pays}?")
