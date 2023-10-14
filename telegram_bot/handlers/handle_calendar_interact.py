from typing import Callable, Any
import datetime
from utils import get_last_week_sunday
from telegram_bot_calendar import DetailedTelegramCalendar
from constants import BOT_START_DATE

LOCALE = 'ru'
DATA_CHOOSE_MESSAGE = "Выбери любой день из нужной недели"

MIN_DATE = datetime.datetime.strptime(BOT_START_DATE, "%Y-%m-%d").date()
MAX_DATE = get_last_week_sunday()


def handle_create_calendar(bot, chat_id):
    calendar, step = DetailedTelegramCalendar(locale=LOCALE, min_date=MIN_DATE, max_date=MAX_DATE).build()
    bot.send_message(chat_id, DATA_CHOOSE_MESSAGE, reply_markup=calendar)


def handle_select_date(bot, call, on_date_selected: Callable[[Any], Any]):
    result, key, step = DetailedTelegramCalendar(locale=LOCALE, min_date=MIN_DATE, max_date=MAX_DATE).process(call.data)
    if not result and key:
        bot.edit_message_text(DATA_CHOOSE_MESSAGE,
                              call.message.chat.id,
                              call.message.message_id,
                              reply_markup=key)
    elif result:
        on_date_selected(result)
