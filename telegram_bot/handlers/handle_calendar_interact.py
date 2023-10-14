from typing import Callable, Any

from telegram_bot_calendar import DetailedTelegramCalendar

LOCALE = 'ru'
DATA_CHOOSE_MESSAGE = "Выбери любой день из нужной недели"


def handle_create_calendar(bot, chat_id):
    calendar, step = DetailedTelegramCalendar(locale=LOCALE).build()
    bot.send_message(chat_id, DATA_CHOOSE_MESSAGE, reply_markup=calendar)


def handle_select_date(bot, call, on_date_selected: Callable[[Any], Any]):
    result, key, step = DetailedTelegramCalendar(locale=LOCALE).process(call.data)
    if not result and key:
        bot.edit_message_text(DATA_CHOOSE_MESSAGE,
                              call.message.chat.id,
                              call.message.message_id,
                              reply_markup=key)
    elif result:
        on_date_selected(result)
