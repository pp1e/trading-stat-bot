import telebot
from config.bot_config import BOT_CONFIG

from constants import DEPOSIT_ACTION, WITHDRAW_ACTION, SELECT_ACTION, WAIT_DEPOSIT

from telegram_bot.handlers.handle_start_command import handle_start_command
from telegram_bot.handlers.handle_week_stat import handle_view_statistic
from telegram_bot.handlers.handle_interact_with_deposit import handle_interact_with_deposit
from telegram_bot.handlers.handle_add_or_withdraw_deposit import handle_add_or_withdraw_deposit
from telegram_bot.handlers.handle_to_start import handle_to_start
from telegram_bot.handlers.handle_select_user import handle_select_user
from telegram_bot.handlers.handle_view_user_deposits import handle_view_user_deposits
from telegram_bot.handlers.handle_deposit import handle_deposit

from telegram_bot.entities.bot_commands import BotCommands


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
        @self.bot.message_handler(commands=[BotCommands.START.value])
        def start(message):
            self.username, self.user_states = (
                handle_start_command(
                    message=message,
                    bot=self.bot,
                    db_connection=self.db_connection,
                    user_states=self.user_states
                ))

        @self.bot.callback_query_handler(func=lambda call: call.data == BotCommands.VIEW_STATISTIC.value)
        def view_statistic_callback(call):
            handle_view_statistic(
                chat_id=call.message.chat.id,
                bot=self.bot,
                db_connection=self.db_connection
            )

        @self.bot.callback_query_handler(func=lambda call: call.data == BotCommands.INTERACT_WITH_DEPOSIT.value)
        def interact_with_deposit_callback(call):
            handle_interact_with_deposit(
                chat_id=call.message.chat.id,
                bot=self.bot,
                db_connection=self.db_connection,
                username=self.username
            )

        @self.bot.callback_query_handler(func=lambda call: call.data == BotCommands.ADD_DEPOSIT.value)
        def add_deposit_callback(call):
            self.operation_type = DEPOSIT_ACTION
            handle_add_or_withdraw_deposit(
                chat_id=call.message.chat.id,
                bot=self.bot,
                db_connection=self.db_connection,
                operation_type=self.operation_type
            )

        @self.bot.callback_query_handler(func=lambda call: call.data == BotCommands.WITHDRAW_MONEY.value)
        def withdraw_money_callback(call):
            self.operation_type = WITHDRAW_ACTION
            handle_add_or_withdraw_deposit(
                chat_id=call.message.chat.id,
                bot=self.bot,
                db_connection=self.db_connection,
                operation_type=self.operation_type
            )

        @self.bot.callback_query_handler(func=lambda call: call.data == BotCommands.TO_START.value)
        def to_start_callback(call):
            self.user_states = handle_to_start(
                chat_id=call.message.chat.id,
                username=self.username,
                user_states=self.user_states,
                bot=self.bot
            )

        @self.bot.callback_query_handler(func=lambda call: call.data.startswith(BotCommands.SELECT_USER.value))
        def select_user_callback(call):
            self.user_states, self.username_pays = (
                handle_select_user(
                    call=call,
                    bot=self.bot,
                    user_states=self.user_states,
                    username=self.username,
                    operation_type=self.operation_type
                ))

        @self.bot.callback_query_handler(func=lambda call: call.data == BotCommands.VIEW_USER_DEPOSITS.value)
        def view_user_deposits_callback(call):
            handle_view_user_deposits(
                chat_id=call.message.chat.id,
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
            self.bot.send_message(message.chat.id, 'Хозяин еще не научил меня этому :(')
