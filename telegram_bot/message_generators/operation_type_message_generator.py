from telegram_bot.entities.bot_commands import BotCommands

from telegram_bot.message_generators.create_buttons import create_buttons


def send_operation_type_message(bot, chat_id, users, message):
    button_parameters = {name: f'select_user_{name}' for name in users}

    button_parameters['Вернуться назад'] = BotCommands.TO_START.value

    markup = create_buttons(button_parameters=button_parameters)

    bot.send_message(chat_id, message, reply_markup=markup)
