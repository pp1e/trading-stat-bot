import sqlite3
from constants import NONAME_ROLE, USER_ROLE, ADMIN_ROLE


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
            balance REAL)
            ''')

        self.cursor.execute("SELECT name FROM sqlite_master WHERE TYPE = 'table' AND NAME = 'weeks_stats';")
        query_result = self.cursor.fetchone()

        if not query_result:
            self.cursor.execute('''
            CREATE TABLE weeks_stats
            (date TEXT PRIMARY KEY,
            overall_balance REAL,
            profit REAL,
            current_week_profit REAL,
            profit_percents REAL, 
            current_week_profit_percents REAL,
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
        self.cursor.execute("INSERT OR IGNORE INTO weeks_stats (date, overall_balance, profit, current_week_profit, "
                            "profit_percents, current_week_profit_percents, user_overall_profits, user_week_profits) "
                            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                            (monday_date, overall_balance, overall_profit, current_week_profit,
                             profit_percents, current_week_profit_percents, user_overall_profits, user_week_profits))
        self.conn.commit()

    def add_new_user(self, username):
        role = NONAME_ROLE
        balance = 0
        self.cursor.execute("INSERT OR IGNORE INTO users_rights (telegram_tag, role, balance) VALUES (?, ?, ?)",
                            (username, role, balance))
        self.conn.commit()

    def is_user_admin(self, username):
        self.cursor.execute("SELECT role FROM users_rights WHERE telegram_tag = ?", (username,))
        role = self.cursor.fetchone()
        if role[0] == ADMIN_ROLE:
            return True
        else:
            return False

    def fetch_user_tags(self):
        self.cursor.execute("SELECT telegram_tag FROM users_rights")
        query_result = self.cursor.fetchall()
        users = [item[0] for item in query_result]
        return users

    def update_balance(self, username_pays, amount):
        self.cursor.execute("UPDATE users_rights SET balance = balance + ? WHERE telegram_tag = ?",
                            (amount, username_pays))
        self.conn.commit()

    def fetch_user_balances(self):
        self.cursor.execute("SELECT telegram_tag, balance FROM users_rights")
        query_result = self.cursor.fetchall()
        result_dict = {}
        for item in query_result:
            key, value = item
            result_dict[key] = value
        return result_dict

    def fetch_week_stat(self, date):
        self.cursor.execute("SELECT * FROM weeks_stats WHERE date = ?", (date,))
        last_row = self.cursor.fetchone()
        return last_row

    def fetch_number_of_week(self):
        self.cursor.execute("SELECT COUNT(*) FROM weeks_stats")
        number_of_week = self.cursor.fetchone()[0] - 1
        print(number_of_week)
        return number_of_week
