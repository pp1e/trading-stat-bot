from constants import BOT_COMMANDS
from tg_bot.bot_utils import create_buttons


def send_welcome_message(bot, message):
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


def handle_echo_message(bot, message):
    bot.send_message(message.chat.id, 'Хозяин еще не научил меня этому :(')
