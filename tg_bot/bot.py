import telebot
from telebot import types

from database import database
from config.bot_config import BOT_CONFIG
from message_printer import message_printer

bot = telebot.TeleBot(BOT_CONFIG['token'])
users = database.database.fetch_user_tags()

select_action = 0
wait_deposit = 1

user_states = {}

username_pays = ''


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Приветик!')
    username = message.from_user.username
    user_states[username] = select_action
    database.database.add_user(username)
    button_message(message)


@bot.message_handler(commands=['button'])
def button_message(message):
    markup = types.InlineKeyboardMarkup()
    stats_button = types.InlineKeyboardButton(text='Посмотреть статистику', callback_data='view_statistic')
    deposit_button = types.InlineKeyboardButton(text='Внести депозит', callback_data='add_deposit')
    markup.add(stats_button)
    markup.add(deposit_button)
    bot.send_message(message.chat.id, text=
    "Я робот-подпилоточник!🤖\nЯ могу ублажать тебя двумя функциями:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == 'view_statistic':
        bot.send_message(call.message.chat.id, message_printer.print_week_statistic(), parse_mode='Markdown')
    elif call.data == 'add_deposit':
        username = call.from_user.username
        if call.data == 'add_deposit':
            if database.database.is_user_admin(username):
                user_deposits_buttons(call.message, users)
                bot.send_message(call.message.chat.id, 'ты не аришка')
                user_states[username] = wait_deposit
            else:
                bot.send_message(call.message.chat.id, 'ты аришка')
    elif call.data == 'to_start':
        button_message(call.message)
    elif call.data.startswith('select_user'):
        global username_pays
        username_pays = call.data.replace('select_user_', '')
        bot.send_message(call.message.chat.id, f"На сколько пополнил {username_pays}?")


@bot.message_handler(func=lambda message: user_states.get(message.from_user.username) == wait_deposit)
def handler_deposit(message):
    try:
        deposit_amount = float(message.text)
        bot.send_message(message.chat.id, f"Пользователь {username_pays} внес {deposit_amount}USD")
        user_states[message.from_user.username] = select_action
        deposit_to_database(deposit_amount)
        button_message(message)
    except ValueError:
        bot.send_message(message.chat.id, "Некорректная сумма. Введите число!")


@bot.message_handler(func=lambda message: user_states.get(message.from_user.username) == select_action)
def echo_message(message):
    bot.send_message(message.chat.id, 'Я тупая аришка. Хозяин еще не научил меня этому :(')


def user_deposits_buttons(message, names):
    markup = types.InlineKeyboardMarkup()
    for name in names:
        callback_data = f'select_user_{name}'
        markup.add(types.InlineKeyboardButton(text=name, callback_data=callback_data))

    markup.add(types.InlineKeyboardButton(text="Вернуться назад", callback_data='to_start'))
    bot.send_message(message.chat.id, 'Кто внес бабло?', reply_markup=markup)


def deposit_to_database(deposit):
    dep_data = [username_pays, deposit]
    database.database.replenishment(dep_data)
