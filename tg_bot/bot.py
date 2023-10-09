import telebot
from config.bot_config import BOT_CONFIG

from tg_bot.handlers.handle_week_stat import handle_view_statistic

from tg_bot.handle_week_stat import handle_view_statistic

from tg_bot.user_actions_handlers import BOT_COMMANDS
from tg_bot.user_actions_handlers import DEPOSIT_ACTION, WITHDRAW_ACTION
from tg_bot.user_actions_handlers import handle_interact_with_deposit
from tg_bot.user_actions_handlers import handle_add_or_withdraw_deposit
from tg_bot.user_actions_handlers import handle_start_command
from tg_bot.user_actions_handlers import SELECT_ACTION, WAIT_DEPOSIT
from tg_bot.user_actions_handlers import handle_to_start
from tg_bot.user_actions_handlers import handle_select_user
from tg_bot.user_actions_handlers import handle_view_user_deposits
from tg_bot.user_actions_handlers import handle_deposit

from tg_bot.bot_messages import handle_echo_message


class TradingStatBot:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.bot = telebot.TeleBot(BOT_CONFIG['token'])
        self.operation_type = None
        self.username_pays = ''
        self.user_states = {}
        self.username = ''

        self.initialize_handlers()

    def initialize_handlers(self):
        @self.bot.message_handler(commands=[BOT_COMMANDS['COMMAND_START']])
        def start(message):
            self.username, self.user_states = handle_start_command(self.bot, self.user_states, self.database, message)

        @self.bot.callback_query_handler(func=lambda call: call.data == BOT_COMMANDS['COMMAND_VIEW_STATISTIC'])
        def view_statistic_callback(call):
            self.username = handle_view_statistic(call, self.bot, self.db_connection)

        @self.bot.callback_query_handler(func=lambda call: call.data == BOT_COMMANDS['COMMAND_INTERACT_WITH_DEPOSIT'])
        def interact_with_deposit_callback(call):
            handle_interact_with_deposit(call, self.bot, self.db_connection)

        @self.bot.callback_query_handler(func=lambda call: call.data == BOT_COMMANDS['COMMAND_ADD_DEPOSIT'])
        def add_deposit_callback(call):
            self.operation_type = DEPOSIT_ACTION
            handle_add_or_withdraw_deposit(call, self.bot, self.db_connection, self.operation_type)

        @self.bot.callback_query_handler(func=lambda call: call.data == BOT_COMMANDS['COMMAND_WITHDRAW_MONEY'])
        def withdraw_money_callback(call):
            self.operation_type = WITHDRAW_ACTION
            handle_add_or_withdraw_deposit(call, self.bot, self.db_connection, self.operation_type)

        @self.bot.callback_query_handler(func=lambda call: call.data == BOT_COMMANDS['COMMAND_TO_START'])
        def to_start_callback(call):
            self.user_states = handle_to_start(call, self.username, self.user_states)

        @self.bot.callback_query_handler(func=lambda call: call.data.startswith(BOT_COMMANDS['COMMAND_SELECT_USER']))
        def select_user_callback(call):
            self.user_states, self.username_pays = handle_select_user(
                call,
                self.bot,
                self.user_states,
                self.username_pays,
                self.username,
                self.operation_type
            )

        @self.bot.callback_query_handler(func=lambda call: call.data == BOT_COMMANDS['COMMAND_VIEW_USER_DEPOSITS'])
        def view_user_deposits_callback(call):
            handle_view_user_deposits(call, self.bot, self.db_connection)

        @self.bot.message_handler(
            func=lambda message: self.user_states.get(self.username) == WAIT_DEPOSIT)
        def deposit_callback(message):
            self.user_states = handle_deposit(
                message,
                self.bot,
                self.db_connection,
                self.username,
                self.user_states,
                self.username_pays,
                self.operation_type
            )

        @self.bot.message_handler(
            func=lambda message: self.user_states.get(self.username) == SELECT_ACTION)
        def echo_message_callback(message):
            handle_echo_message(self.bot, message)
