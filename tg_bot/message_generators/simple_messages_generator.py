from constants import DEPOSIT_ACTION, WITHDRAW_ACTION


def send_operation_type_message(operation_type, bot, call, markup):
    if operation_type == DEPOSIT_ACTION:
        bot.send_message(call.message.chat.id, 'Кто пополнил балик?', reply_markup=markup)
    else:
        bot.send_message(call.message.chat.id, 'Кто снял деньги?', reply_markup=markup)


def send_operation_result_message(operation_type, bot, message, username_pays, deposit_amount):
    if operation_type == DEPOSIT_ACTION:
        bot.send_message(message.chat.id, f"Пользователь {username_pays} "
                                          f"внес {deposit_amount}USD")
    elif operation_type == WITHDRAW_ACTION:
        bot.send_message(message.chat.id, f"Пользователь {username_pays} "
                                          f"снял {deposit_amount}USD")


def send_user_rights(bot, call, markup):
    if markup is not None:
        bot.send_message(call.message.chat.id, 'Я могу выполнить эти функции', reply_markup=markup)
    else:
        bot.send_message(call.message.chat.id, 'У вас нет прав для этих действий')


def send_transaction_amount_question(operation_type, bot, call, username_pays):
    if operation_type == DEPOSIT_ACTION:
        bot.send_message(call.message.chat.id, f"На сколько пополнил {username_pays}?")
    elif operation_type == WITHDRAW_ACTION:
        bot.send_message(call.message.chat.id, f"Сколько снял {username_pays}?")
