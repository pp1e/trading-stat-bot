import json
import time

from bs4 import BeautifulSoup
from pyppeteer import launch
import asyncio
import constants


def dollarsToNumber(dollars):
    return float(dollars.replace(' ', '').replace('$', '').replace(',', ''))


def percentsToNumber(percents):
    return float(percents.replace('+', '').replace('%', ''))


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
        with open(constants.DATA_FILE, 'w') as dataFile:
            data = asyncio.run(scrapData())
            dataFile.write(json.dumps(data))
        print('Data was scrapped!')
        time.sleep(60)
