import datetime
import json

import telebot
from telebot import types

from config.bot_config import BOT_CONFIG
from message_printer import message_printer
from config.storage_config import STORAGE_CONFIG
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
        self.operation_type = None

        @self.bot.message_handler(commands=['start'])
        def start(message):
            self.bot.send_message(message.chat.id, 'Приветик!')
            username = message.from_user.username
            user_states[username] = select_action
            self.database.add_new_user(username)
            button_message(message)

        @self.bot.message_handler(commands=['button'])
        def button_message(message):
            markup = types.InlineKeyboardMarkup()
            stats_button = types.InlineKeyboardButton(text='Посмотреть статистику', callback_data='view_statistic')
            interact_with_deposit_button = types.InlineKeyboardButton(text='Депозит',
                                                                      callback_data='interact_with_deposit')
            markup.add(stats_button)
            markup.add(interact_with_deposit_button)
            self.bot.send_message(message.chat.id,
                                  text="Я робот-подпилоточник!🤖\nЯ могу ублажать тебя двумя функциями:",
                                  reply_markup=markup)

        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_handler(call):
            if call.data == 'view_statistic':
                current_week_monday = utils.get_current_monday_date()
                if utils.is_today_weekends():
                    data = self.database.fetch_week_stat(current_week_monday)
                    if data is None:
                        past_week_monday = current_week_monday - datetime.timedelta(days=7)
                        data = self.database.fetch_week_stat(past_week_monday)
                        screenshot = self.load_screenshot(past_week_monday)
                    else:
                        screenshot = self.load_screenshot(current_week_monday)
                else:
                    past_week_monday = current_week_monday - datetime.timedelta(days=7)
                    data = self.database.fetch_week_stat(past_week_monday)
                    screenshot = self.load_screenshot(past_week_monday)

                user_deposits = self.database.fetch_user_deposits()
                message = message_printer.print_week_statistic(
                    date=data[0],
                    week_profit_percets=data[5],
                    user_overall_profits=json.loads(data[6]),
                    user_week_profits=json.loads(data[7]),
                    user_deposits=user_deposits,
                    week_profit=data[3],
                    total_profit=data[1],
                )

                self.bot.send_photo(
                    chat_id=call.message.chat.id,
                    photo=screenshot,
                    caption=message,
                    parse_mode='html',
                )

            elif call.data == 'interact_with_deposit':
                username = call.from_user.username
                if self.database.is_user_admin(username):
                    self.create_actions_with_deposit(call.message)
                    user_states[username] = wait_deposit
                    self.bot.send_message(call.message.chat.id, 'ты не фембойчик')
                else:
                    self.bot.send_message(call.message.chat.id, 'ты фембойчик')

            elif call.data == 'add_deposit':
                self.operation_type = 'deposit'
                self.create_user_deposits_button(call.message, self.users)

            elif call.data == 'withdraw_money':
                self.operation_type = 'withdraw'
                self.create_user_deposits_button(call.message, self.users)

            elif call.data == 'to_start':
                button_message(call.message)

            elif call.data.startswith('select_user'):
                global username_pays
                username_pays = call.data.replace('select_user_', '')
                if self.operation_type == 'deposit':
                    self.bot.send_message(call.message.chat.id, f"На сколько пополнил {username_pays}?")
                elif self.operation_type == 'withdraw':
                    self.bot.send_message(call.message.chat.id, f"Сколько снял {username_pays}?")

            elif call.data == 'view_user_deposits':
                user_deposits = self.database.fetch_user_deposits()
                message = message_printer.print_user_deposits_info(user_deposits)
                self.bot.send_message(call.message.chat.id, message, parse_mode='html')

        @self.bot.message_handler(func=lambda message: user_states.get(message.from_user.username) == wait_deposit)
        def handler_deposit(message):
            try:
                print(user_states)
                deposit_amount = float(message.text)
                if deposit_amount >= 0:
                    if self.operation_type == 'deposit':
                        self.bot.send_message(message.chat.id, f"Пользователь {username_pays} "
                                                               f"внес {deposit_amount}USD")
                        self.send_user_replenishment_to_database(deposit_amount)
                    elif self.operation_type == 'withdraw':
                        self.bot.send_message(message.chat.id, f"Пользователь {username_pays} "
                                                               f"снял {deposit_amount}USD")
                        self.send_user_replenishment_to_database(-deposit_amount)
                else:
                    self.bot.send_message(message.chat.id, "Сумма не может быть отрицательной!")
                button_message(message)
            except ValueError:
                self.bot.send_message(message.chat.id, "Некорректная сумма. Введите число!")

        @self.bot.message_handler(func=lambda message: user_states.get(message.from_user.username) == select_action)
        def echo_message(message):
            self.bot.send_message(message.chat.id, 'Я тупой фембойчик. Хозяин еще не научил меня этому :(')

    def create_user_deposits_button(self, message, names):
        markup = types.InlineKeyboardMarkup()
        for name in names:
            callback_data = f'select_user_{name}'
            markup.add(types.InlineKeyboardButton(text=name, callback_data=callback_data))

        markup.add(types.InlineKeyboardButton(text="Вернуться назад", callback_data='to_start'))

        if self.operation_type == 'deposit':
            self.bot.send_message(message.chat.id, 'Кто пополнил балик?', reply_markup=markup)
        elif self.operation_type == 'withdraw':
            self.bot.send_message(message.chat.id, 'Кто снял деньги?', reply_markup=markup)

    def send_user_replenishment_to_database(self, deposit):
        self.database.replenish_deposit(username_pays, deposit)

    def load_screenshot(self, screen_date):
        return open(f'{STORAGE_CONFIG["path_to_screens"]}/{screen_date}.png', 'rb')

    def create_actions_with_deposit(self, message):
        markup = types.InlineKeyboardMarkup()
        add_deposit_button = types.InlineKeyboardButton(text='Пополнить баланс', callback_data='add_deposit')
        withdraw_money_button = types.InlineKeyboardButton(text='Снять деньги', callback_data='withdraw_money')
        view_user_deposits = types.InlineKeyboardButton(text='Посмотреть информацию о депозитах',
                                                        callback_data='view_user_deposits')
        markup.add(add_deposit_button)
        markup.add(withdraw_money_button)
        markup.add(view_user_deposits)

        self.bot.send_message(message.chat.id, 'Я могу выполнить эти функции', reply_markup=markup)
