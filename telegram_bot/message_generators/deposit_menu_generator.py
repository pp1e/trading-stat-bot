from telegram_bot.entities.bot_commands import BotCommands

from telegram_bot.message_generators.create_buttons import create_buttons


def send_user_deposit_menu(bot, chat_id):
    markup = create_buttons(
        button_parameters={
            'Пополнить баланс': BotCommands.ADD_DEPOSIT.value,
            'Снять деньги': BotCommands.WITHDRAW_MONEY.value,
            'Вернуться назад': BotCommands.TO_START.value
        }
    )

    bot.send_message(chat_id, 'Я могу выполнить эти функции', reply_markup=markup)
