import json
import time
import traceback

from bs4 import BeautifulSoup
from pyppeteer import launch
import asyncio

import utils
from config.storage_config import STORAGE_CONFIG
from database.create_connection import create_db_connection
from database import users_rights_table
from database import weeks_stats_table
from incomes_calculations.calculate_week_profit import calculate_week_user_profits
from utils import is_today_weekends, get_current_week_monday


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
    time.sleep(10)

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
    db_connection = create_db_connection()
    while True:
        if is_today_weekends():
            try:
                data = asyncio.run(scrap_data())
                if data:
                    user_balances = users_rights_table.fetch_user_balances(db_connection)
                    last_week_stat = weeks_stats_table.fetch_week_stat(db_connection, utils.get_last_week_monday())

                    user_overall_profits, user_week_profits = calculate_week_user_profits(
                        actual_overall_balance=data["overall_balance"],
                        last_week_user_balances=user_balances,
                        last_week_user_overall_profits=json.loads(last_week_stat[6]),
                    )

                    is_current_week_stat_not_in_db = weeks_stats_table.fetch_week_stat(
                        db_connection, utils.get_current_week_monday()
                    ) is None

                    if is_current_week_stat_not_in_db:
                        weeks_stats_table.insert_week_profit(
                            db_connection=db_connection,
                            monday_date=get_current_week_monday(),
                            overall_balance=data["overall_balance"],
                            overall_profit=data["profit"],
                            current_week_profit=data["current_week_profit"],
                            profit_percents=data["profit_percents"],
                            current_week_profit_percents=data["current_week_profit_percents"],
                            user_overall_profits=json.dumps(user_overall_profits),
                            user_week_profits=json.dumps(user_week_profits),
                        )
                        for user_tag, user_week_profit in user_week_profits.items():
                            users_rights_table.update_balance(db_connection, user_tag, user_week_profit)

                    print('Data was scrapped successfully!')
                else:
                    print("Data was not scrapped :(")
            except Exception:
                traceback.print_exc()
                print("Error while scrapping data!")

        time.sleep(600)
