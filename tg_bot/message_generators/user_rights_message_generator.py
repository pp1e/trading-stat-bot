from tg_bot.entities.bot_commands import BotCommands

from tg_bot.message_generators.create_buttons import create_buttons


def send_user_rights(bot, chat_id):
    markup = create_buttons(
        button_parameters={
            'Пополнить баланс': BotCommands.ADD_DEPOSIT.value,
            'Снять деньги': BotCommands.WITHDRAW_MONEY.value,
            'Посмотреть информацию о балансах': BotCommands.VIEW_USER_DEPOSITS.value,
            'Вернуться назад': BotCommands.TO_START.value
        }
    )

    bot.send_message(chat_id, 'Я могу выполнить эти функции', reply_markup=markup)
