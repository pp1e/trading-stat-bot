import json
import telebot
from telebot import types
from config.bot_config import BOT_CONFIG
from message_printer import message_printer
from config.storage_config import STORAGE_CONFIG
from constants import SELECT_ACTION, WAIT_DEPOSIT
import utils


class TradingStatBot:
    def __init__(self, data_base):
        self.database = data_base
        self.users = self.database.fetch_user_tags()
        self.bot = telebot.TeleBot(BOT_CONFIG['token'])
        self.operation_type = None
        self.username_pays = ''
        self.user_states = {}

        self.initialize_handlers()

    def initialize_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            self.handle_start_command(message)

        @self.bot.callback_query_handler(func=lambda call: call.data == 'view_statistic')
        def view_statistic_callback(call):
            self.handle_view_statistic(call)

        @self.bot.callback_query_handler(func=lambda call: call.data == 'interact_with_deposit')
        def interact_with_deposit_callback(call):
            self.handle_interact_with_deposit(call)

        @self.bot.callback_query_handler(func=lambda call: call.data == 'add_deposit')
        def add_deposit_callback(call):
            self.handle_add_deposit(call)

        @self.bot.callback_query_handler(func=lambda call: call.data == 'withdraw_money')
        def withdraw_money_callback(call):
            self.handle_withdraw_money(call)

        @self.bot.callback_query_handler(func=lambda call: call.data == 'to_start')
        def to_start_callback(call):
            self.handle_to_start(call)

        @self.bot.callback_query_handler(func=lambda call: call.data.startswith('select_user'))
        def select_user_callback(call):
            self.handle_select_user(call)

        @self.bot.callback_query_handler(func=lambda call: call.data == 'view_user_deposits')
        def view_user_deposits_callback(call):
            self.handle_view_user_deposits(call)

        @self.bot.message_handler(func=lambda message: self.user_states.get(message.from_user.username) == WAIT_DEPOSIT)
        def deposit_callback(message):
            self.handle_deposit(message)

        @self.bot.message_handler(func=lambda message: self.user_states.get(message.from_user.username) == SELECT_ACTION)
        def echo_message_callback(message):
            self.handle_echo_message(message)

    def handle_start_command(self, message):
        self.bot.send_message(message.chat.id, 'Приветик!')
        username = message.from_user.username
        self.user_states[username] = SELECT_ACTION
        self.database.add_new_user(username)
        self.send_welcome_message(message)

    def handle_view_statistic(self, call):
        current_week_monday = utils.get_current_week_monday()
        if utils.is_today_weekends():
            data = self.database.fetch_week_stat(current_week_monday)
            if data is None:
                last_week_monday = utils.get_last_week_monday()
                data = self.database.fetch_week_stat(last_week_monday)
                screenshot = self.load_screenshot(last_week_monday)
            else:
                screenshot = self.load_screenshot(current_week_monday)
        else:
            last_week_monday = utils.get_last_week_monday()
            data = self.database.fetch_week_stat(last_week_monday)
            screenshot = self.load_screenshot(last_week_monday)

        user_balances = self.database.fetch_user_balances()
        message = message_printer.print_week_statistic(
            date=data[0],
            week_profit_percents=data[5],
            user_overall_profits=json.loads(data[6]),
            user_week_profits=json.loads(data[7]),
            user_balances=user_balances,
            week_profit=data[3],
            overall_balance=data[1],
            overall_profit=data[2],
        )

        self.bot.send_photo(
            chat_id=call.message.chat.id,
            photo=screenshot,
            caption=message,
            parse_mode='html',
        )

    def handle_interact_with_deposit(self, call):
        username = call.from_user.username
        if self.database.is_user_admin(username):
            self.create_actions_with_deposit(call.message)
            self.user_states[username] = WAIT_DEPOSIT
            self.bot.send_message(call.message.chat.id, 'У вас есть права для изменения данных')
        else:
            self.bot.send_message(call.message.chat.id, 'У вас нет прав для этих действий')

    def handle_add_deposit(self, call):
        self.operation_type = 'deposit'
        self.create_user_deposits_button(call.message, self.users)

    def handle_withdraw_money(self, call):
        self.operation_type = 'withdraw'
        self.create_user_deposits_button(call.message, self.users)

    def handle_to_start(self, call):
        self.send_welcome_message(call.message)

    def handle_select_user(self, call):
        self.username_pays = call.data.replace('select_user_', '')
        if self.operation_type == 'deposit':
            self.bot.send_message(call.message.chat.id, f"На сколько пополнил {self.username_pays}?")
        elif self.operation_type == 'withdraw':
            self.bot.send_message(call.message.chat.id, f"Сколько снял {self.username_pays}?")

    def handle_view_user_deposits(self, call):
        user_balances = self.database.fetch_user_balances()
        message = message_printer.print_user_balances_info(user_balances)
        self.bot.send_message(call.message.chat.id, message, parse_mode='html')
        self.send_welcome_message(call.message)

    def handle_deposit(self, message):
        try:
            deposit_amount = float(message.text)
            if deposit_amount >= 0:
                if self.operation_type == 'deposit':
                    self.bot.send_message(message.chat.id, f"Пользователь {self.username_pays} "
                                                           f"внес {deposit_amount}USD")
                    self.database.update_balance(self.username_pays, deposit_amount)
                elif self.operation_type == 'withdraw':
                    self.bot.send_message(message.chat.id, f"Пользователь {self.username_pays} "
                                                           f"снял {deposit_amount}USD")
                    self.database.update_balance(self.username_pays, -deposit_amount)
            else:
                self.bot.send_message(message.chat.id, "Сумма не может быть отрицательной!")
            self.send_welcome_message(message)
        except ValueError:
            self.bot.send_message(message.chat.id, "Некорректная сумма. Введите число!")

    def handle_echo_message(self, message):
        self.bot.send_message(message.chat.id, 'Хозяин еще не научил меня этому :(')

    def send_welcome_message(self, message):
        welcome_text = "Я робот-подпилоточник!🤖\nЯ могу ублажать тебя двумя функциями:"
        markup = self.create_welcome_inline_buttons()
        self.bot.send_message(message.chat.id,
                              text=welcome_text,
                              reply_markup=markup)

    def create_welcome_inline_buttons(self):
        markup = types.InlineKeyboardMarkup()

        buttons = [
            types.InlineKeyboardButton(text='Посмотреть статистику', callback_data='view_statistic'),
            types.InlineKeyboardButton(text='Депозит', callback_data='interact_with_deposit')
        ]

        for button in buttons:
            markup.add(button)

        return markup

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

    def load_screenshot(self, screen_date):
        return open(f'{STORAGE_CONFIG["path_to_screens"]}/{screen_date}.png', 'rb')

    def create_actions_with_deposit(self, message):
        markup = types.InlineKeyboardMarkup()

        buttons = [
            types.InlineKeyboardButton(text='Пополнить баланс', callback_data='add_deposit'),
            types.InlineKeyboardButton(text='Снять деньги', callback_data='withdraw_money'),
            types.InlineKeyboardButton(text='Посмотреть информацию о балансах', callback_data='view_user_deposits'),
            types.InlineKeyboardButton(text="Вернуться назад", callback_data='to_start')
        ]

        for button in buttons:
            markup.add(button)

        self.bot.send_message(message.chat.id, 'Я могу выполнить эти функции', reply_markup=markup)
