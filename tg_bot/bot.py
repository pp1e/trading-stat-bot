import telebot
from config.bot_config import BOT_CONFIG

from constants import BOT_COMMANDS, DEPOSIT_ACTION, WITHDRAW_ACTION, SELECT_ACTION, WAIT_DEPOSIT

from tg_bot.handlers.handle_start_command import handle_start_command
from tg_bot.handlers.handle_week_stat import handle_view_statistic
from tg_bot.handlers.handle_interact_with_deposit import handle_interact_with_deposit
from tg_bot.handlers.handle_add_or_withdraw_deposit import handle_add_or_withdraw_deposit
from tg_bot.handlers.handle_to_start import handle_to_start
from tg_bot.handlers.handle_select_user import handle_select_user
from tg_bot.handlers.handle_view_user_deposits import handle_view_user_deposits
from tg_bot.handlers.handle_deposit import handle_deposit

from tg_bot.message_generators.echo_message_generator import handle_echo_message


class TradingStatBot:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.bot = telebot.TeleBot(BOT_CONFIG['token'])
        self.operation_type = None
        self.username_pays = ''
        self.user_states = {}
        self.username = None

        self.initialize_handlers()

    def initialize_handlers(self):
        @self.bot.message_handler(commands=[BOT_COMMANDS['COMMAND_START']])
        def start(message):
            self.username, self.user_states = (
                handle_start_command(
                    message=message,
                    bot=self.bot,
                    db_connection=self.db_connection,
                    user_states=self.user_states
                ))

        @self.bot.callback_query_handler(func=lambda call: call.data == BOT_COMMANDS['COMMAND_VIEW_STATISTIC'])
        def view_statistic_callback(call):
            handle_view_statistic(
                call=call,
                bot=self.bot,
                db_connection=self.db_connection
            )

        @self.bot.callback_query_handler(func=lambda call: call.data == BOT_COMMANDS['COMMAND_INTERACT_WITH_DEPOSIT'])
        def interact_with_deposit_callback(call):
            handle_interact_with_deposit(
                call=call,
                bot=self.bot,
                db_connection=self.db_connection,
                username=self.username
            )

        @self.bot.callback_query_handler(func=lambda call: call.data == BOT_COMMANDS['COMMAND_ADD_DEPOSIT'])
        def add_deposit_callback(call):
            self.operation_type = DEPOSIT_ACTION
            handle_add_or_withdraw_deposit(
                call=call,
                bot=self.bot,
                db_connection=self.db_connection,
                operation_type=self.operation_type
            )

        @self.bot.callback_query_handler(func=lambda call: call.data == BOT_COMMANDS['COMMAND_WITHDRAW_MONEY'])
        def withdraw_money_callback(call):
            self.operation_type = WITHDRAW_ACTION
            handle_add_or_withdraw_deposit(
                call=call,
                bot=self.bot,
                db_connection=self.db_connection,
                operation_type=self.operation_type
            )

        @self.bot.callback_query_handler(func=lambda call: call.data == BOT_COMMANDS['COMMAND_TO_START'])
        def to_start_callback(call):
            self.user_states = handle_to_start(
                call=call,
                username=self.username,
                user_states=self.user_states,
                bot=self.bot
            )

        @self.bot.callback_query_handler(func=lambda call: call.data.startswith(BOT_COMMANDS['COMMAND_SELECT_USER']))
        def select_user_callback(call):
            self.user_states, self.username_pays = (
                handle_select_user(
                    call=call,
                    bot=self.bot,
                    user_states=self.user_states,
                    username=self.username,
                    operation_type=self.operation_type
                ))

        @self.bot.callback_query_handler(func=lambda call: call.data == BOT_COMMANDS['COMMAND_VIEW_USER_DEPOSITS'])
        def view_user_deposits_callback(call):
            handle_view_user_deposits(
                call=call,
                bot=self.bot,
                db_connection=self.db_connection
            )

        @self.bot.message_handler(
            func=lambda message: self.user_states.get(self.username) == WAIT_DEPOSIT)
        def deposit_callback(message):
            self.user_states = (
                handle_deposit(
                    message=message,
                    bot=self.bot,
                    db_connection=self.db_connection,
                    username=self.username,
                    user_states=self.user_states,
                    username_pays=self.username_pays,
                    operation_type=self.operation_type
                ))

        @self.bot.message_handler(func=lambda message: self.user_states.get(self.username) == SELECT_ACTION)
        def echo_message_callback(message):
            handle_echo_message(
                bot=self.bot,
                message=message
            )
