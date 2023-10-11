from constants import BOT_COMMANDS
from tg_bot.handlers.create_buttons import create_buttons


def send_welcome_message(bot, message):
    bot.send_message(message.chat.id, 'Приветик!')

    welcome_text = "Я робот-подпилоточник!🤖\nЯ могу ублажать тебя двумя функциями:"

    markup = create_buttons(
        button_parameters={
            'Посмотреть статистику': BOT_COMMANDS['COMMAND_VIEW_STATISTIC'],
            'Депозит': BOT_COMMANDS['COMMAND_INTERACT_WITH_DEPOSIT'],
        })

    bot.send_message(
        message.chat.id,
        text=welcome_text,
        reply_markup=markup
    )
