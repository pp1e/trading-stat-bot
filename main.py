import json
import time
from json import JSONDecodeError
from multiprocessing import Process

import telebot
from telebot import types
from bs4 import BeautifulSoup
from pyppeteer import launch
import asyncio


ALEX_DEP = 753
IVAN_DEP = 600
DENIS_DEP = 100
OVERALL_DEP = ALEX_DEP + IVAN_DEP + DENIS_DEP
DATA_FILE = 'data.json'

bot = telebot.TeleBot('6511544558:AAGZOxhdStzt6SLpe14FgSPwJ84ncThxqJw')


def dollarsToNumber(dollars):
    return float(dollars.replace(' ', '').replace('$', '').replace(',', ''))


def percentsToNumber(percents):
    return float(percents.replace('+','').replace('%', ''))


async def scrapData():
    url = 'https://fxmonitor.online/a/17542800?view=pro&mode=2'

    # # Launch the browser
    browser = await launch()

    # Open a new browser page
    page = await browser.newPage()

    # Open our test file in the opened page
    await page.goto(url)

    # Wait for all dynamic data to load
    time.sleep(1)

    # Get page source code
    page_content = await page.content()

    await browser.close()

    soup = BeautifulSoup(page_content, 'lxml')
    return {
        "balance": dollarsToNumber(soup.find('a', id='17542800balance').text),
        "profit": dollarsToNumber(soup.find('span', id='17542800profit_total').text),
        "currentWeekProfit": dollarsToNumber(soup.find('span', id='17542800profit_w').text),
        #"lastWeekProfit": "",
        "profitPercents": percentsToNumber(soup.find('span', id='17542800profit_w_pr').text),
        "currentWeekProfitPercents": percentsToNumber(soup.find('span', id='17542800profit_w_pr').text),
    }


def scrapDataProcess():
    while True:
        with open(DATA_FILE, 'w') as dataFile:
            data = asyncio.run(scrapData())
            dataFile.write(json.dumps(data))
        print('Data was scrapped!')
        time.sleep(60)


def calcAnte(balance, dep):
    return round(balance * (dep / OVERALL_DEP), 2)


def generateStatistic():
    with open(DATA_FILE, 'r') as dataFile:
        data = json.loads(dataFile.read())

    balance = data['balance']
    currentWeekProfit = data['currentWeekProfit']
    profit = data['profit']

    return f"""
** ТЕКУЩАЯ НЕДЕЛЯ **

**Заработано за неделю:**
+{data['currentWeekProfitPercents']}% | +${currentWeekProfit}

🔹**Ваня: +${calcAnte(currentWeekProfit, IVAN_DEP)}**
Депозит: ${IVAN_DEP}
Текущий баланс: ${calcAnte(balance, IVAN_DEP)}
Общая прибыль: +${calcAnte(profit, IVAN_DEP)}

🔹**Саня: +${calcAnte(currentWeekProfit, ALEX_DEP)}**
Депозит: ${ALEX_DEP}
Текущий баланс: ${calcAnte(balance, ALEX_DEP)}
Общая прибыль: +${calcAnte(profit, ALEX_DEP)}

🔹**Ден: +${calcAnte(currentWeekProfit, DENIS_DEP)}**
Депозит: ${DENIS_DEP}
Текущий баланс: ${calcAnte(balance, DENIS_DEP)}
Общая прибыль: +${calcAnte(profit, DENIS_DEP)}

**Всего:** ${OVERALL_DEP} -> ${balance}

[СЛЕДИТЬ](https://fxmonitor.online/u/UQEvKqKD?view=pro)
        """

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    statBtn = types.KeyboardButton("Посмотреть статистику")
    markup.add(statBtn)
    bot.send_message(message.chat.id, "Я робот-долбоеб!🤖", reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    try:
        if message.text == "Посмотреть статистику":
            bot.send_message(message.chat.id, generateStatistic(), parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, 'иди нахуй')
    except JSONDecodeError:
        bot.send_message(message.chat.id, 'Ошибка при извлечении данных! Попробуй еще раз')



# chromeDriver = ChromeDriverManager().install()
# print(chromeDriver)
# service=ChromeService(chromeDriver)
# print(service)
# driver = webdriver.Chrome(service=service)
#
# driver.get(url)
# htmlText = driver.page_source
#
# print(htmlText)
# soup = BeautifulSoup(htmlText, 'lxml')
# print(soup.find('a', id='17542800profit_d'))

#data = asyncio.run(scrapData())

# print(asyncio.run(scrapData()))
scrapProcess = Process(target=scrapDataProcess)
scrapProcess.start()
bot.polling(none_stop=True, interval=0)
