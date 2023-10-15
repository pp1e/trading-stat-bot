import functools

import telebot.types

from database import users_rights_table


def admin_required_factory(bot=None, db_connection=None):
    def admin_required(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            username = args[0].from_user.username

            if type(args[0]) is telebot.types.CallbackQuery:
                chat_id = args[0].message.chat.id
            else:
                chat_id = args[0].chat.id

            if username is None:
                bot.send_message(chat_id, 'Установите имя пользователя в настройках!')
            else:
                if users_rights_table.is_user_admin(db_connection=db_connection, username=username):
                    func(*args, **kwargs)
                else:
                    bot.send_message(chat_id, 'У вас нет доступа к моим функциям!')

        return wrapper

    return admin_required
