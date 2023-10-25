from telegram_bot.entities.bot_commands import BotCommands

from telegram_bot.message_generators.create_buttons import create_buttons


def send_user_statistic_menu(bot, chat_id):
    markup = create_buttons(
        button_parameters={
            'Актуальная статистика': BotCommands.VIEW_ACTUAL_STATISTIC.value,
            'Статистика за выбранную неделю': BotCommands.VIEW_SPECIFIED_STATISTIC.value,
            'Статистика по депозитам': BotCommands.VIEW_DEPOSIT_STATISTIC.value,
            'Вернуться назад': BotCommands.TO_START.value
        }
    )

    bot.send_message(chat_id, 'Я могу выполнить эти функции', reply_markup=markup)
