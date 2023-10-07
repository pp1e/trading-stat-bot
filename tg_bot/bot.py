import telebot
from telebot import types
from config.bot_config import BOT_CONFIG
from message_generator import user_balances_generator
import utils
from tg_bot.handle_week_stat import handle_view_statistic

SELECT_ACTION = 0
WAIT_DEPOSIT = 1

COMMAND_START = 'start'
COMMAND_VIEW_STATISTIC = 'view_statistic'
COMMAND_INTERACT_WITH_DEPOSIT = 'interact_with_deposit'
COMMAND_ADD_DEPOSIT = 'add_deposit'
COMMAND_WITHDRAW_MONEY = 'withdraw_money'
COMMAND_TO_START = 'to_start'
COMMAND_SELECT_USER = 'select_user'
COMMAND_VIEW_USER_DEPOSITS = 'view_user_deposits'

DEPOSIT_ACTION = 'deposit'
WITHDRAW_ACTION = 'withdraw'


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
        @self.bot.message_handler(commands=[COMMAND_START])
        def start(message):
            self.handle_start_command(message)

        @self.bot.callback_query_handler(func=lambda call: call.data == COMMAND_VIEW_STATISTIC)
        def view_statistic_callback(call):
            handle_view_statistic(call, self.bot, self.database)

        @self.bot.callback_query_handler(func=lambda call: call.data == COMMAND_INTERACT_WITH_DEPOSIT)
        def interact_with_deposit_callback(call):
            self.handle_interact_with_deposit(call)

        @self.bot.callback_query_handler(func=lambda call: call.data == COMMAND_ADD_DEPOSIT)
        def add_deposit_callback(call):
            self.handle_add_deposit(call)

        @self.bot.callback_query_handler(func=lambda call: call.data == COMMAND_WITHDRAW_MONEY)
        def withdraw_money_callback(call):
            self.handle_withdraw_money(call)

        @self.bot.callback_query_handler(func=lambda call: call.data == COMMAND_TO_START)
        def to_start_callback(call):
            self.handle_to_start(call)

        @self.bot.callback_query_handler(func=lambda call: call.data.startswith(COMMAND_SELECT_USER))
        def select_user_callback(call):
            self.handle_select_user(call)

        @self.bot.callback_query_handler(func=lambda call: call.data == COMMAND_VIEW_USER_DEPOSITS)
        def view_user_deposits_callback(call):
            self.handle_view_user_deposits(call)

        @self.bot.message_handler(func=lambda message: self.user_states.get(message.from_user.username) == WAIT_DEPOSIT)
        def deposit_callback(message):
            self.handle_deposit(message)

        @self.bot.message_handler(
            func=lambda message: self.user_states.get(message.from_user.username) == SELECT_ACTION)
        def echo_message_callback(message):
            self.handle_echo_message(message)

    def handle_start_command(self, message):
        self.bot.send_message(message.chat.id, 'Приветик!')
        username = message.from_user.username
        self.user_states[username] = SELECT_ACTION
        self.database.add_new_user(username)
        self.send_welcome_message(message)

    def handle_interact_with_deposit(self, call):
        username = call.from_user.username
        if self.database.is_user_admin(username):
            button_parameters = {
                'Пополнить баланс': COMMAND_ADD_DEPOSIT,
                'Снять деньги': COMMAND_WITHDRAW_MONEY,
                'Посмотреть информацию о балансах': COMMAND_VIEW_USER_DEPOSITS,
                'Вернуться назад': COMMAND_TO_START
            }
            markup = self.create_buttons(button_parameters)
            self.bot.send_message(call.message.chat.id, 'Я могу выполнить эти функции', reply_markup=markup)
            self.user_states[username] = WAIT_DEPOSIT
            self.bot.send_message(call.message.chat.id, 'У вас есть права для изменения данных')
        else:
            self.bot.send_message(call.message.chat.id, 'У вас нет прав для этих действий')

    def handle_add_deposit(self, call):
        self.operation_type = DEPOSIT_ACTION

        button_parameters = {}

        for name in self.users:
            callback_data = f'select_user_{name}'
            button_parameters[name] = callback_data

        button_parameters['Вернуться назад'] = COMMAND_TO_START

        markup = self.create_buttons(button_parameters)

        self.bot.send_message(call.message.chat.id, 'Кто пополнил балик?', reply_markup=markup)

    def handle_withdraw_money(self, call):
        button_parameters = {}

        for name in self.users:
            callback_data = f'select_user_{name}'
            button_parameters[name] = callback_data

        button_parameters['Вернуться назад'] = COMMAND_TO_START

        markup = self.create_buttons(button_parameters)

        self.bot.send_message(call.message.chat.id, 'Кто снял деньги?', reply_markup=markup)

    def handle_to_start(self, call):
        self.send_welcome_message(call.message)

    def handle_select_user(self, call):
        self.username_pays = call.data.replace('select_user_', '')
        if self.operation_type == DEPOSIT_ACTION:
            self.bot.send_message(call.message.chat.id, f"На сколько пополнил {self.username_pays}?")
        elif self.operation_type == WITHDRAW_ACTION:
            self.bot.send_message(call.message.chat.id, f"Сколько снял {self.username_pays}?")

    def handle_view_user_deposits(self, call):
        user_balances = self.database.fetch_user_balances()
        message = user_balances_generator.form_user_balances_info(user_balances)
        self.bot.send_message(call.message.chat.id, message, parse_mode='html')
        self.send_welcome_message(call.message)

    def handle_deposit(self, message):
        try:
            deposit_amount = float(message.text)

            if deposit_amount >= 0:
                if self.operation_type == DEPOSIT_ACTION:
                    self.bot.send_message(message.chat.id, f"Пользователь {self.username_pays} "
                                                           f"внес {deposit_amount}USD")
                    self.database.update_balance(self.username_pays, deposit_amount)
                elif self.operation_type == WITHDRAW_ACTION:
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

        button_parameters = {
            'Посмотреть статистику': COMMAND_VIEW_STATISTIC,
            'Депозит': COMMAND_INTERACT_WITH_DEPOSIT,
        }

        markup = self.create_buttons(button_parameters)

        self.bot.send_message(message.chat.id,
                              text=welcome_text,
                              reply_markup=markup)

    def create_buttons(self, button_parameters):
        markup = types.InlineKeyboardMarkup()

        for key in button_parameters.keys():
            markup.add(types.InlineKeyboardButton(text=key, callback_data=button_parameters[key]))

        return markup