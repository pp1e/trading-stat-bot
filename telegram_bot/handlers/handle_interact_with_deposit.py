from database import users_rights_table

from telegram_bot.message_generators.user_deposit_menu_generator import send_user_deposit_menu


def handle_interact_with_deposit(chat_id, bot, db_connection, username):
    if username is None:
        bot.send_message(chat_id, 'Установите имя пользователя в настройках телеграмма или перезапустите меня!')
    else:
        check_user_rights(
            chat_id=chat_id,
            bot=bot,
            db_connection=db_connection,
            username=username
        )


def check_user_rights(chat_id, bot, db_connection, username):
    if users_rights_table.is_user_admin(db_connection=db_connection, username=username):
        send_user_deposit_menu(bot=bot, chat_id=chat_id)
    else:
        bot.send_message(chat_id, 'У вас нет прав для этих действий')
