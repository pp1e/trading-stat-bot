import datetime
import sqlite3
from utils import get_current_monday_date


class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE TYPE = 'table' AND NAME = 'users_rights';")
        query_result = self.cursor.fetchone()

        if not query_result:
            self.cursor.execute('''
            CREATE TABLE users_rights
            (telegram_tag TEXT PRIMARY KEY,
            role TEXT,
            deposit REAL)
            ''')

        self.cursor.execute("SELECT name FROM sqlite_master WHERE TYPE = 'table' AND NAME = 'weeks_stats';")
        query_result = self.cursor.fetchone()

        if not query_result:
            self.cursor.execute('''
            CREATE TABLE weeks_stats
            (date TEXT PRIMARY KEY,
            balance REAL,
            profit REAL,
            currentWeekProfit REAL,
            profitPercents REAL, 
            currentWeekProfitPercents REAL,
            user_overall_profits TEXT,
            user_week_profits TEXT)
            ''')

        self.cursor.execute("SELECT name FROM sqlite_master WHERE TYPE = 'table' AND NAME = 'deposits_info';")
        query_result = self.cursor.fetchone()

        if not query_result:
            self.cursor.execute('''
            CREATE TABLE deposits_info
            (id INTEGER PRIMARY KEY,
            telegram_tag TEXT,
            date TEXT,
            user_rubles_deposit REAL,
            dollar_price REAL,
            dollar_amount REAL,
            FOREIGN KEY (telegram_tag) REFERENCES user_rights(telegram_tag))
            ''')

        self.conn.commit()

    def insert_week_profit(self, monday_date, overall_balance, overall_profit, current_week_profit,
                           profit_percents, current_week_profit_percents, user_overall_profits, user_week_profits):
        self.cursor.execute("INSERT OR IGNORE INTO weeks_stats (date, balance, profit, currentWeekProfit, "
                            "profitPercents, currentWeekProfitPercents, user_overall_profits, user_week_profits) "
                            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                            (monday_date, overall_balance, overall_profit, current_week_profit,
                             profit_percents, current_week_profit_percents, user_overall_profits, user_week_profits))
        self.conn.commit()

    def add_user(self, username):
        role = 'noname'
        deposit = 0
        self.cursor.execute("INSERT OR IGNORE INTO users_rights (telegram_tag, role, deposit) VALUES (?, ?, ?)",
                            (username, role, deposit))
        self.conn.commit()

    def is_user_admin(self, username):
        self.cursor.execute("SELECT role FROM users_rights WHERE telegram_tag = ?", (username,))
        role = self.cursor.fetchone()
        if role[0] == 'admin':
            return True
        else:
            return False

    def fetch_user_tags(self):
        self.cursor.execute("SELECT telegram_tag FROM users_rights")
        query_result = self.cursor.fetchall()
        users = [item[0] for item in query_result]
        return users

    def replenishment(self, data):
        self.cursor.execute("UPDATE users_rights SET deposit = deposit + ? WHERE telegram_tag = ?",
                            (data[1], data[0]))
        self.conn.commit()

    def fetch_user_deposits(self):
        self.cursor.execute("SELECT telegram_tag, deposit FROM users_rights")
        query_result = self.cursor.fetchall()
        result_dict = {}
        for item in query_result:
            key, value = item
            result_dict[key] = value
        return result_dict

    def fetch_week_profit(self):
        current_week_monday = get_current_monday_date()
        self.cursor.execute("SELECT currentWeekProfit FROM weeks_stats WHERE date = ?", (current_week_monday,))
        query_result = self.cursor.fetchone()
        week_result = query_result[0]
        return week_result

    def add_data(self, json_data):
        current_week_monday = get_current_monday_date()
        self.cursor.execute("UPDATE weeks_stats SET user_overall_profits = ? WHERE date = ?", (json_data, current_week_monday))
        self.conn.commit()

    def fetch_user_overall_profits(self):
        previous_week_monday = get_current_monday_date() - datetime.timedelta(days=7)
        self.cursor.execute("SELECT user_overall_profits FROM weeks_stats WHERE date = ?", (previous_week_monday,))
        query_result = self.cursor.fetchone()
        return query_result[0]

    def fetch_last_week_row(self):
        current_week_monday = get_current_monday_date()
        self.cursor.execute("SELECT * FROM weeks_stats WHERE date = ?", (current_week_monday,))
        last_row = self.cursor.fetchone()
        return last_row
