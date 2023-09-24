import datetime
import json

import telebot
from telebot import types

from config.bot_config import BOT_CONFIG
from message_printer import message_printer
import utils


select_action = 0
wait_deposit = 1

user_states = {}

username_pays = ''


class TradingStatBot:
    def __init__(self, data_base):
        self.database = data_base
        self.users = self.database.fetch_user_tags()
        self.bot = telebot.TeleBot(BOT_CONFIG['token'])

        @self.bot.message_handler(commands=['start'])
        def start(message):
            self.bot.send_message(message.chat.id, 'Приветик!')
            username = message.from_user.username
            user_states[username] = select_action
            self.database.add_user(username)
            button_message(message)

        @self.bot.message_handler(commands=['button'])
        def button_message(message):
            markup = types.InlineKeyboardMarkup()
            stats_button = types.InlineKeyboardButton(text='Посмотреть статистику', callback_data='view_statistic')
            deposit_button = types.InlineKeyboardButton(text='Внести депозит', callback_data='add_deposit')
            markup.add(stats_button)
            markup.add(deposit_button)
            self.bot.send_message(message.chat.id, text=
            "Я робот-подпилоточник!🤖\nЯ могу ублажать тебя двумя функциями:", reply_markup=markup)

        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_handler(call):
            if call.data == 'view_statistic':
                current_week_monday = utils.get_current_monday_date()
                if utils.is_today_weekends():
                    data = self.database.fetch_week_stat(current_week_monday)
                else:
                    data = self.database.fetch_week_stat(current_week_monday - datetime.timedelta(days=7))

                user_deposits = self.database.fetch_user_deposits()
                message = message_printer.print_week_statistic(
                    date=data[0],
                    week_profit_percets=data[5],
                    user_overall_profits=json.loads(data[6]),
                    user_week_profits = json.loads(data[7]),
                    user_deposits=user_deposits,
                    week_profit=data[3],
                    total_profit=data[1],
                )

                self.bot.send_message(call.message.chat.id, message, parse_mode='html')
            elif call.data == 'add_deposit':
                username = call.from_user.username
                if call.data == 'add_deposit':
                    if self.database.is_user_admin(username):
                        self.user_deposits_buttons(call.message, self.users)
                        self.bot.send_message(call.message.chat.id, 'ты не аришка')
                        user_states[username] = wait_deposit
                    else:
                        self.bot.send_message(call.message.chat.id, 'ты аришка')
            elif call.data == 'to_start':
                button_message(call.message)
            elif call.data.startswith('select_user'):
                global username_pays
                username_pays = call.data.replace('select_user_', '')
                self.bot.send_message(call.message.chat.id, f"На сколько пополнил {username_pays}?")

        @self.bot.message_handler(func=lambda message: user_states.get(message.from_user.username) == wait_deposit)
        def handler_deposit(message):
            try:
                deposit_amount = float(message.text)
                self.bot.send_message(message.chat.id, f"Пользователь {username_pays} внес {deposit_amount}USD")
                user_states[message.from_user.username] = select_action
                self.deposit_to_database(deposit_amount)
                button_message(message)
            except ValueError:
                self.bot.send_message(message.chat.id, "Некорректная сумма. Введите число!")

        @self.bot.message_handler(func=lambda message: user_states.get(message.from_user.username) == select_action)
        def echo_message(message):
            self.bot.send_message(message.chat.id, 'Я тупая аришка. Хозяин еще не научил меня этому :(')

    def user_deposits_buttons(self, message, names):
        markup = types.InlineKeyboardMarkup()
        for name in names:
            callback_data = f'select_user_{name}'
            markup.add(types.InlineKeyboardButton(text=name, callback_data=callback_data))

        markup.add(types.InlineKeyboardButton(text="Вернуться назад", callback_data='to_start'))
        self.bot.send_message(message.chat.id, 'Кто внес бабло?', reply_markup=markup)

    def deposit_to_database(self, deposit):
        dep_data = [username_pays, deposit]
        self.database.replenishment(dep_data)
