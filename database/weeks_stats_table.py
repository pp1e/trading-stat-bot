def create_table(db_connection):
    cursor = db_connection.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE TYPE = 'table' AND NAME = 'weeks_stats';")
    query_result = cursor.fetchone()

    if not query_result:
        cursor.execute('''
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

    db_connection.commit()


def insert_week_profit(db_connection, monday_date, overall_balance, overall_profit, current_week_profit,
                       profit_percents, current_week_profit_percents, user_overall_profits, user_week_profits):
    cursor = db_connection.cursor()

    cursor.execute("INSERT OR IGNORE INTO weeks_stats (date, overall_balance, profit, current_week_profit, "
                   "profit_percents, current_week_profit_percents, user_overall_profits, user_week_profits) "
                   "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   (monday_date, overall_balance, overall_profit, current_week_profit,
                    profit_percents, current_week_profit_percents, user_overall_profits, user_week_profits))
    db_connection.commit()


def fetch_week_stat(db_connection, date):
    cursor = db_connection.cursor()

    cursor.execute("SELECT * FROM weeks_stats WHERE date = ?", (date,))
    last_row = cursor.fetchone()
    return last_row


def fetch_week_number(db_connection, week_monday):
    cursor = db_connection.cursor()

    cursor.execute(f"SELECT stat.date, stat.row_number FROM "
                   f"(SELECT ROW_NUMBER() OVER (ORDER BY date) AS row_number, date FROM weeks_stats)"
                   f" stat WHERE date = ?", (week_monday,))
    number_of_week = cursor.fetchone()[1] - 1
    return number_of_week

