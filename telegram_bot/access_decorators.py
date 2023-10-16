from functools import wraps

from database import users_rights_table


def admin_message_required_factory(bot=None, db_connection=None):
    def admin_required(func):
        @wraps(func)
        def wrapper(message):
            username = message.from_user.username

            if username is None:
                bot.send_message(message.chat.id, 'Установите имя пользователя в настройках!')
            else:
                if users_rights_table.is_user_admin(db_connection=db_connection, username=username):
                    func(message)
                else:
                    bot.send_message(message.chat.id, 'У вас нет доступа к моим функциям!')

        return wrapper

    return admin_required


def admin_call_required_factory(bot=None, db_connection=None):
    def admin_required(func):
        @wraps(func)
        def wrapper(call):
            username = call.from_user.username

            if username is None:
                bot.send_message(call.message.chat.id, 'Установите имя пользователя в настройках!')
            else:
                if users_rights_table.is_user_admin(db_connection=db_connection, username=username):
                    func(call)
                else:
                    bot.send_message(call.message.chat.id, 'У вас нет доступа к моим функциям!')

        return wrapper

    return admin_required
