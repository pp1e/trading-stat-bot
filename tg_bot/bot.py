import json
from json import JSONDecodeError

import telebot
from telebot import types

import constants
from database import database
from config.bot_config import BOT_CONFIG


bot = telebot.TeleBot(BOT_CONFIG['token'])


def calcAnte(balance, dep):
    return round(balance * (dep / constants.OVERALL_DEP), 2)


def generateStatistic():
    with open(constants.DATA_FILE, 'r') as dataFile:
        data = json.loads(dataFile.read())

    balance = data['balance']
    currentWeekProfit = data['currentWeekProfit']
    profit = data['profit']

    return f"""
** ТЕКУЩАЯ НЕДЕЛЯ **

**Заработано за неделю:**
+{data['currentWeekProfitPercents']}% | +${currentWeekProfit}

🔹**Ваня: +${calcAnte(currentWeekProfit, constants.IVAN_DEP)}**
Депозит: ${constants.IVAN_DEP}
Текущий баланс: ${calcAnte(balance, constants.IVAN_DEP)}
Общая прибыль: +${calcAnte(profit, constants.IVAN_DEP)}

🔹**Саня: +${calcAnte(currentWeekProfit, constants.ALEX_DEP)}**
Депозит: ${constants.ALEX_DEP}
Текущий баланс: ${calcAnte(balance, constants.ALEX_DEP)}
Общая прибыль: +${calcAnte(profit, constants.ALEX_DEP)}

🔹**Ден: +${calcAnte(currentWeekProfit, constants.DENIS_DEP)}**
Депозит: ${constants.DENIS_DEP}
Текущий баланс: ${calcAnte(balance, constants.DENIS_DEP)}
Общая прибыль: +${calcAnte(profit, constants.DENIS_DEP)}

**Всего:** ${constants.OVERALL_DEP} -> ${balance}

[СЛЕДИТЬ](https://fxmonitor.online/u/UQEvKqKD?view=pro)
        """


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Приветик!')
    username = message.from_user.username
    database.database.add_user(username)
    button_message(message)

@bot.message_handler(commands=['button'])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    statButton = types.KeyboardButton("Посмотреть статистику")
    depositButton = types.KeyboardButton("Внести депозит")
    markup.add(statButton)
    markup.add(depositButton)
    bot.send_message(message.chat.id, "Я робот-подпилоточник!🤖", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    try:
        if message.text == "Посмотреть статистику":
            bot.send_message(message.chat.id, generateStatistic(), parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, 'иди нахуй')
    except JSONDecodeError:
        bot.send_message(message.chat.id, 'Ошибка при извлечении данных! Попробуй еще раз')

    try:
        if message.text == "Внести депозит":
            username = message.from_user.username
            if database.database.check_rules(username):
                users = database.database.unique_users()
                deposit_buttons(message, users)
            else:
                bot.send_message(message.chat.id, 'ты аришка')
    except JSONDecodeError:
        bot.send_message(message.chat.id, 'Ошибка при извлечении данных! Попробуй еще раз')
@bot.message_handler(content_types='text')
def deposit_buttons(message, names):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in names:
        markup.add(types.KeyboardButton(*name))
    bot.send_message(message.chat.id, 'Кто внес бабло?', reply_markup=markup)
