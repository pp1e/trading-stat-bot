import telebot
from telegram_bot_calendar import DetailedTelegramCalendar

from config.bot_config import BOT_CONFIG

from constants import DEPOSIT_ACTION, WITHDRAW_ACTION, SELECT_ACTION, WAIT_DOLLAR_DEPOSIT, WAIT_RUBLE_DEPOSIT

from telegram_bot.handlers.handle_start_command import handle_start_command
from telegram_bot.handlers.handle_week_stat import handle_view_last_statistic, handle_view_specified_statistic
from telegram_bot.handlers.handle_calendar_interact import handle_select_date, handle_create_calendar
from telegram_bot.handlers.handle_view_deposit_menu import handle_view_deposit_menu
from telegram_bot.handlers.handle_view_statistic_menu import handle_view_statistic_menu
from telegram_bot.handlers.handle_add_or_withdraw_deposit import handle_add_or_withdraw_deposit
from telegram_bot.handlers.handle_to_start import handle_to_start
from telegram_bot.handlers.handle_select_user import handle_select_user
from telegram_bot.handlers.handle_deposit import handle_dollar_deposit, handle_ruble_deposit
from telegram_bot.handlers.handle_average_dollar_price import handle_average_dollar_price
from telegram_bot.entities.bot_commands import BotCommands

from telegram_bot.access_decorators import admin_message_required_factory, admin_call_required_factory


class TradingStatBot:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.bot = telebot.TeleBot(BOT_CONFIG['token'])
        self.unique_user_transaction = {}
        self.user_states = {}
        self.admin_required_message = admin_message_required_factory(db_connection=self.db_connection, bot=self.bot)
        self.admin_required_call = admin_call_required_factory(db_connection=self.db_connection, bot=self.bot)

        self.initialize_handlers()

    def initialize_handlers(self):
        @self.bot.message_handler(commands=[BotCommands.START.value])
        @self.admin_required_message
        def start(message):
            self.user_states = (
                handle_start_command(
                    message=message,
                    bot=self.bot,
                    user_states=self.user_states
                ))

        @self.bot.callback_query_handler(func=lambda call: call.data == BotCommands.VIEW_STATISTIC.value)
        @self.admin_required_call
        def view_statistic_menu_callback(call):
            handle_view_statistic_menu(
                chat_id=call.message.chat.id,
                bot=self.bot
            )

        @self.bot.callback_query_handler(func=lambda call: call.data == BotCommands.VIEW_ACTUAL_STATISTIC.value)
        @self.admin_required_call
        def view_last_statistic_callback(call):
            handle_view_last_statistic(
                chat_id=call.message.chat.id,
                bot=self.bot,
                db_connection=self.db_connection
            )

        @self.bot.callback_query_handler(func=lambda call: call.data == BotCommands.VIEW_SPECIFIED_STATISTIC.value)
        @self.admin_required_call
        def view_specified_statistic_callback(call):
            handle_create_calendar(
                bot=self.bot,
                chat_id=call.message.chat.id
            )

        @self.bot.callback_query_handler(func=DetailedTelegramCalendar.func())
        @self.admin_required_call
        def select_date_callback(call):
            handle_select_date(
                bot=self.bot,
                call=call,
                on_date_selected=lambda date: handle_view_specified_statistic(
                    db_connection=self.db_connection,
                    chat_id=call.message.chat.id,
                    bot=self.bot,
                    week_date=date
                )
            )

        @self.bot.callback_query_handler(func=lambda call: call.data == BotCommands.INTERACT_WITH_DEPOSIT.value)
        @self.admin_required_call
        def view_deposit_menu_callback(call):
            self.unique_user_transaction[call.from_user.username] = {}
            handle_view_deposit_menu(
                chat_id=call.message.chat.id,
                bot=self.bot,
            )

        @self.bot.callback_query_handler(func=lambda call: call.data == BotCommands.ADD_DEPOSIT.value)
        @self.admin_required_call
        def add_deposit_callback(call):
            self.unique_user_transaction[call.from_user.username]['operation_type'] = DEPOSIT_ACTION
            handle_add_or_withdraw_deposit(
                chat_id=call.message.chat.id,
                bot=self.bot,
                db_connection=self.db_connection,
                operation_type=self.unique_user_transaction[call.from_user.username]['operation_type']
            )

        @self.bot.callback_query_handler(func=lambda call: call.data == BotCommands.WITHDRAW_MONEY.value)
        @self.admin_required_call
        def withdraw_money_callback(call):
            self.unique_user_transaction[call.from_user.username]['operation_type'] = WITHDRAW_ACTION
            handle_add_or_withdraw_deposit(
                chat_id=call.message.chat.id,
                bot=self.bot,
                db_connection=self.db_connection,
                operation_type=self.unique_user_transaction[call.from_user.username]['operation_type']
            )

        @self.bot.callback_query_handler(
            func=lambda call: call.data == BotCommands.VIEW_AVERAGE_PURCHASE_DOLLAR_PRICE.value)
        @self.admin_required_call
        def view_average_dollar_price(call):
            handle_average_dollar_price(
                bot=self.bot,
                chat_id=call.message.chat.id,
                db_connection=self.db_connection
            )

        @self.bot.callback_query_handler(func=lambda call: call.data == BotCommands.TO_START.value)
        @self.admin_required_call
        def to_start_callback(call):
            self.user_states, self.unique_user_transaction = handle_to_start(
                chat_id=call.message.chat.id,
                username=call.from_user.username,
                user_states=self.user_states,
                bot=self.bot,
                unique_user_transaction=self.unique_user_transaction
            )

        @self.bot.callback_query_handler(func=lambda call: call.data.startswith(BotCommands.SELECT_USER.value))
        @self.admin_required_call
        def select_user_callback(call):
            self.unique_user_transaction[call.from_user.username] = (
                handle_select_user(
                    call=call,
                    bot=self.bot,
                    user_states=self.user_states,
                    username=call.from_user.username,
                    unique_user_transaction=self.unique_user_transaction[call.from_user.username]
                ))

        @self.bot.message_handler(
            func=lambda message: self.user_states.get(message.from_user.username) == WAIT_DOLLAR_DEPOSIT)
        @self.admin_required_message
        def dollar_deposit_callback(message):
            self.user_states, self.unique_user_transaction = (
                handle_dollar_deposit(
                    message=message,
                    bot=self.bot,
                    db_connection=self.db_connection,
                    username=message.from_user.username,
                    user_states=self.user_states,
                    unique_user_transaction=self.unique_user_transaction
                ))

        @self.bot.message_handler(
            func=lambda message: self.user_states.get(message.from_user.username) == WAIT_RUBLE_DEPOSIT)
        @self.admin_required_message
        def ruble_deposit_callback(message):
            self.user_states, self.unique_user_transaction = (
                handle_ruble_deposit(
                    message=message,
                    bot=self.bot,
                    db_connection=self.db_connection,
                    username=message.from_user.username,
                    user_states=self.user_states,
                    unique_user_transaction=self.unique_user_transaction
                ))

        @self.bot.message_handler(
            func=lambda message: self.user_states.get(message.from_user.username) == SELECT_ACTION)
        @self.admin_required_message
        def echo_message_callback(message):
            self.bot.send_message(message.chat.id, 'Хозяин еще не научил меня этому :(')
