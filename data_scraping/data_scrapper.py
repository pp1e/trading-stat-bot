import json
import time

from bs4 import BeautifulSoup
from pyppeteer import launch
import asyncio
from incomes_calculations.calc_module import calculate_week_user_profits
from utils import is_today_weekends, get_current_monday_date


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
        "profitPercents": percentsToNumber(soup.find('span', id='17542800profit_total_pr').text),
        "currentWeekProfitPercents": percentsToNumber(soup.find('span', id='17542800profit_w_pr').text),
    }


def scrapDataProcess(database):
    while True:
        if is_today_weekends():
            data = asyncio.run(scrapData())
            if data:
                user_deposits = database.fetch_user_deposits()
                user_overall_profits = database.fetch_user_overall_profits()
                user_overall_profits = json.loads(user_overall_profits)
                user_overall_profits, user_week_profits = calculate_week_user_profits(
                    data["currentWeekProfit"], user_deposits, user_overall_profits
                )

                database.insert_week_profit(
                    monday_date=get_current_monday_date(),
                    overall_balance=data["balance"],
                    overall_profit=data["profit"],
                    current_week_profit=data["currentWeekProfit"],
                    profit_percents=data["profitPercents"],
                    current_week_profit_percents=data["currentWeekProfitPercents"],
                    user_overall_profits=json.dumps(user_overall_profits),
                    user_week_profits=json.dumps(user_week_profits),
                )
                print('Data was scrapped!')
            else:
                print("Scrapy died!")

        time.sleep(600)
