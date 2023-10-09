from tg_bot.bot_utils import create_buttons
from tg_bot.bot_messages import send_welcome_message
from message_generator.user_balances_generator import form_user_balances_info

BOT_COMMANDS = {
    'COMMAND_START': 'start',
    'COMMAND_VIEW_STATISTIC': 'view_statistic',
    'COMMAND_INTERACT_WITH_DEPOSIT': 'interact_with_deposit',
    'COMMAND_ADD_DEPOSIT': 'add_deposit',
    'COMMAND_WITHDRAW_MONEY': 'withdraw_money',
    'COMMAND_TO_START': 'to_start',
    'COMMAND_SELECT_USER': 'select_user',
    'COMMAND_VIEW_USER_DEPOSITS': 'view_user_deposits',
}

SELECT_ACTION = 0
WAIT_DEPOSIT = 1

DEPOSIT_ACTION = 'deposit'
WITHDRAW_ACTION = 'withdraw'


def handle_start_command(bot, user_states, database, message):
    bot.send_message(message.chat.id, 'Приветик!')
    username = message.from_user.username
    user_states[username] = SELECT_ACTION
    database.add_new_user(username)
    send_welcome_message(bot, message)

    return username, user_states


def handle_to_start(call, username, user_states):
    user_states[username] = SELECT_ACTION
    send_welcome_message(call.message)
    return user_states


def handle_interact_with_deposit(call, bot, database):
    # TODO: подумать нужен ли этот username вообще
    username = call.from_user.username

    if database.is_user_admin(username):
        markup = create_buttons(
            button_parameters={
                'Пополнить баланс': BOT_COMMANDS['COMMAND_ADD_DEPOSIT'],
                'Снять деньги': BOT_COMMANDS['COMMAND_WITHDRAW_MONEY'],
                'Посмотреть информацию о балансах': BOT_COMMANDS['COMMAND_VIEW_USER_DEPOSITS'],
                'Вернуться назад': BOT_COMMANDS['COMMAND_TO_START']
            }
        )

        bot.send_message(call.message.chat.id, 'Я могу выполнить эти функции', reply_markup=markup)
    else:
        bot.send_message(call.message.chat.id, 'У вас нет прав для этих действий')

    return username


def handle_add_or_withdraw_deposit(call, bot, database, operation_type):
    users = database.fetch_user_tags()

    button_parameters = {name: f'select_user_{name}' for name in users}

    button_parameters['Вернуться назад'] = BOT_COMMANDS['COMMAND_TO_START']

    markup = create_buttons(button_parameters)

    if operation_type == DEPOSIT_ACTION:
        bot.send_message(call.message.chat.id, 'Кто пополнил балик?', reply_markup=markup)
    else:
        bot.send_message(call.message.chat.id, 'Кто снял деньги?', reply_markup=markup)


def handle_view_user_deposits(call, bot, database):
    user_balances = database.fetch_user_balances()
    message = form_user_balances_info(user_balances)
    bot.send_message(call.message.chat.id, message, parse_mode='html')
    send_welcome_message(call.message)


def handle_select_user(call, bot, user_states, username, operation_type):
    username_pays = call.data.replace('select_user_', '')
    user_states[username] = WAIT_DEPOSIT
    if operation_type == DEPOSIT_ACTION:
        bot.send_message(call.message.chat.id, f"На сколько пополнил {username_pays}?")
    elif operation_type == WITHDRAW_ACTION:
        bot.send_message(call.message.chat.id, f"Сколько снял {username_pays}?")


def handle_deposit(message, bot, database, username, user_states, username_pays, operation_type):
    try:
        deposit_amount = float(message.text)

        if deposit_amount >= 0:
            if operation_type == DEPOSIT_ACTION:
                bot.send_message(message.chat.id, f"Пользователь {username_pays} "
                                                  f"внес {deposit_amount}USD")
                database.update_balance(username_pays, deposit_amount)
            elif operation_type == WITHDRAW_ACTION:
                bot.send_message(message.chat.id, f"Пользователь {username_pays} "
                                                  f"снял {deposit_amount}USD")
                database.update_balance(username_pays, -deposit_amount)
        else:
            bot.send_message(message.chat.id, "Сумма не может быть отрицательной!")

        user_states[username] = SELECT_ACTION

        send_welcome_message(message)
    except ValueError:
        bot.send_message(message.chat.id, "Некорректная сумма. Введите число!")
