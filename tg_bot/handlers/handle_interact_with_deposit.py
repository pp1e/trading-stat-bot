from database import users_rights_table

from tg_bot.message_generators.simple_messages_generator import send_user_rights


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
    if users_rights_table.is_user_admin(db_connection=db_connection, username=username):
        send_user_rights(bot=bot, call=call)
    else:
        bot.send_message(call.message.chat.id, 'У вас нет прав для этих действий')
