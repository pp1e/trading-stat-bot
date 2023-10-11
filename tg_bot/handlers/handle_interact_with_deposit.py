from constants import BOT_COMMANDS
from database import users_rights_table
from tg_bot.handlers.create_buttons import create_buttons


def handle_interact_with_deposit(call, bot, db_connection, username):
    if username is None:
        bot.send_message(call.message.chat.id, 'Установите имя пользователя в настройках телеграмма')
    else:
        check_user_rights(
            call=call,
            bot=bot,
            db_connection=db_connection,
            username=username
        )


def check_user_rights(call, bot, db_connection, username):
    if users_rights_table.is_user_admin(db_connection, username):

        markup = create_buttons(
            button_parameters={
                'Пополнить баланс': BOT_COMMANDS['COMMAND_ADD_DEPOSIT'],
                'Снять деньги': BOT_COMMANDS['COMMAND_WITHDRAW_MONEY'],
                'Посмотреть информацию о балансах': BOT_COMMANDS['COMMAND_VIEW_USER_DEPOSITS'],
                'Вернуться назад': BOT_COMMANDS['COMMAND_TO_START']
            }
        )

        bot.send_message(call.message.chat.id, 'Я могу выполнить эти функции', reply_markup=markup)
    else:
        bot.send_message(call.message.chat.id, 'У вас нет прав для этих действий')
