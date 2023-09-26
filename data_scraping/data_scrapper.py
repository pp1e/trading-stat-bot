import json
import time
import traceback

from bs4 import BeautifulSoup
from pyppeteer import launch
import asyncio

from config.storage_config import STORAGE_CONFIG
from incomes_calculations.calc_module import calculate_week_user_profits
from utils import is_today_weekends, get_current_monday_date
from database.database import Database


def dollars_to_number(dollars):
    return float(dollars.replace(' ', '').replace('$', '').replace(',', ''))


def percents_to_number(percents):
    return float(percents.replace('+', '').replace('%', ''))


async def scrap_data():
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

    current_week_monday = get_current_monday_date()
    # Get screenshot of the page
    await page.screenshot({'path': f'{STORAGE_CONFIG["path_to_screens"]}/{current_week_monday}.png'})

    await browser.close()

    soup = BeautifulSoup(page_content, 'lxml')
    return {
        "balance": dollars_to_number(soup.find('a', id='17542800balance').text),
        "profit": dollars_to_number(soup.find('span', id='17542800profit_total').text),
        "currentWeekProfit": dollars_to_number(soup.find('span', id='17542800profit_w').text),
        "profitPercents": percents_to_number(soup.find('span', id='17542800profit_total_pr').text),
        "currentWeekProfitPercents": percents_to_number(soup.find('span', id='17542800profit_w_pr').text),
    }


def scrap_data_process():
    database = Database(STORAGE_CONFIG['name'])
    while True:
        if is_today_weekends():
            try:
                data = asyncio.run(scrap_data())
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
                    print('Data was scrapped successfully!')
                else:
                    print("Data was not scrapped :(")
            except Exception as e:
                traceback.print_exc()
                print("Error while scrapping data!")

        time.sleep(600)
