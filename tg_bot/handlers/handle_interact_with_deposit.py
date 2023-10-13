from database import users_rights_table

from tg_bot.message_generators.user_rights_message_generator import send_user_rights


def handle_interact_with_deposit(chat_id, bot, db_connection, username):
    if username is None:
        bot.send_message(chat_id, 'Установите имя пользователя в настройках телеграмма')
    else:
        check_user_rights(
            chat_id=chat_id,
            bot=bot,
            db_connection=db_connection,
            username=username
        )


def check_user_rights(chat_id, bot, db_connection, username):
    if users_rights_table.is_user_admin(db_connection=db_connection, username=username):
        send_user_rights(bot=bot, chat_id=chat_id)
    else:
        bot.send_message(chat_id, 'У вас нет прав для этих действий')
