import sqlite3
from config.db_config import DB_CONFIG


class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
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
            user_part TEXT)
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


database = Database(DB_CONFIG['name'])
