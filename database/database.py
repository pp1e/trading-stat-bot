import sqlite3
from config.db_config import DB_CONFIG
from datetime import date


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

    def insert_week_profit(self, data):
        today = date.today()
        data = [*data.values()]
        self.cursor.execute("INSERT OR IGNORE INTO weeks_stats (date, balance, profit, currentWeekProfit, "
                            "profitPercents, currentWeekProfitPercents) VALUES (?, ?, ?, ?, ?, ?)",
                            (today, data[0], data[1], data[2], data[3], data[4]))
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


database = Database(DB_CONFIG['name'])
