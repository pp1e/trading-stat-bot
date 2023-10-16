from functools import wraps
from constants import ADMIN_ROLE
from database import users_rights_table


def admin_message_required_factory(bot=None, db_connection=None):
    def admin_required(func):
        @wraps(func)
        def wrapper(message):
            username = message.from_user.username
            chat_id = message.chat.id

            if is_user_admin(bot=bot, chat_id=chat_id, db_connection=db_connection, username=username):
                func(message)

        return wrapper

    return admin_required


def admin_call_required_factory(bot=None, db_connection=None):
    def admin_required(func):
        @wraps(func)
        def wrapper(call):
            username = call.from_user.username
            chat_id = call.message.chat.id

            if is_user_admin(bot=bot, chat_id=chat_id, db_connection=db_connection, username=username):
                func(call)

        return wrapper

    return admin_required


def is_user_admin(bot, chat_id, db_connection, username):
    if username is None:
        bot.send_message(chat_id, 'Установите имя пользователя в настройках!')
        return False

    role = users_rights_table.fetch_user_role(db_connection=db_connection, username=username)

    if role and role[0] == ADMIN_ROLE:
        return True

    bot.send_message(chat_id, 'У вас нет доступа к моим функциям!')
    return False
