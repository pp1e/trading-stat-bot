from telegram_bot.entities.bot_commands import BotCommands

from telegram_bot.message_generators.create_buttons import create_buttons


def send_welcome_message(bot, chat_id):
    bot.send_message(chat_id, 'Приветик!')

    welcome_text = "Я робот-подпилоточник!🤖\nЯ могу ублажать тебя двумя функциями:"

    markup = create_buttons(
        button_parameters={
            'Посмотреть статистику': BotCommands.VIEW_STATISTIC.value,
            'Депозит': BotCommands.INTERACT_WITH_DEPOSIT.value,
        })

    bot.send_message(
        chat_id,
        text=welcome_text,
        reply_markup=markup
    )
