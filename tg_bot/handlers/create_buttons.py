from telebot import types


def create_buttons(button_parameters):
    markup = types.InlineKeyboardMarkup()

    for key in button_parameters.keys():
        markup.add(types.InlineKeyboardButton(text=key, callback_data=button_parameters[key]))

    return markup
