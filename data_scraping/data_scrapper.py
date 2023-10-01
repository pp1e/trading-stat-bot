import json
import time
import traceback

from bs4 import BeautifulSoup
from pyppeteer import launch
import asyncio

import utils
from config.storage_config import STORAGE_CONFIG
from incomes_calculations.calc_module import calculate_week_user_profits
from utils import is_today_weekends, get_current_week_monday
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

    current_week_monday = get_current_week_monday()
    # Get screenshot of the page
    await page.screenshot({'path': f'{STORAGE_CONFIG["path_to_screens"]}/{current_week_monday}.png'})

    await browser.close()

    soup = BeautifulSoup(page_content, 'lxml')
    return {
        "overall_balance": dollars_to_number(soup.find('a', id='17542800balance').text),
        "profit": dollars_to_number(soup.find('span', id='17542800profit_total').text),
        "current_week_profit": dollars_to_number(soup.find('span', id='17542800profit_w').text),
        "profit_percents": percents_to_number(soup.find('span', id='17542800profit_total_pr').text),
        "current_week_profit_percents": percents_to_number(soup.find('span', id='17542800profit_w_pr').text),
    }


def scrap_data_process():
    database = Database(STORAGE_CONFIG['name'])
    while True:
        if is_today_weekends():
            try:
                data = asyncio.run(scrap_data())
                if data:
                    overall_balance = data["overall_balance"]

                    user_balances = database.fetch_user_balances()
                    last_week_stat = database.fetch_week_stat(utils.get_last_week_monday())

                    user_overall_profits, user_week_profits = calculate_week_user_profits(
                        actual_overall_balance=overall_balance,
                        last_week_overall_balance=last_week_stat[1],
                        user_balances=user_balances,
                        last_week_user_overall_profits=json.loads(last_week_stat[6]),
                    )

                    is_current_week_stat_not_in_db = database.fetch_week_stat(utils.get_current_week_monday()) is None

                    if is_current_week_stat_not_in_db:
                        database.insert_week_profit(
                            monday_date=get_current_week_monday(),
                            overall_balance=overall_balance,
                            overall_profit=data["profit"],
                            current_week_profit=data["current_week_profit"],
                            profit_percents=data["profit_percents"],
                            current_week_profit_percents=data["current_week_profit_percents"],
                            user_overall_profits=json.dumps(user_overall_profits),
                            user_week_profits=json.dumps(user_week_profits),
                        )
                        for user_tag, user_week_profit in user_week_profits.items():
                            database.update_balance(user_tag, user_week_profit)

                    print('Data was scrapped successfully!')
                else:
                    print("Data was not scrapped :(")
            except Exception:
                traceback.print_exc()
                print("Error while scrapping data!")

        time.sleep(600)
