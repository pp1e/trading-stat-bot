def create_table(db_connection):
    cursor = db_connection.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE TYPE = 'table' AND NAME = 'deposits_info';")
    query_result = cursor.fetchone()

    if not query_result:
        cursor.execute('''
        CREATE TABLE deposits_info
        (id INTEGER PRIMARY KEY,
        telegram_tag TEXT,
        date TEXT,
        user_rubles_deposit REAL,
        dollar_price REAL,
        dollar_amount REAL,
        FOREIGN KEY (telegram_tag) REFERENCES user_rights(telegram_tag))
        ''')

    db_connection.commit()


def fetch_user_deposits(db_connection):
    cursor = db_connection.cursor()

    cursor.execute("SELECT telegram_tag, SUM(user_rubles_deposit), SUM(dollar_amount) "
                   "FROM deposits_info GROUP BY telegram_tag")

    query_result = cursor.fetchall()

    return query_result


def insert_deposit(db_connection, id, telegram_tag, date, user_rubles_deposit, dollar_price, dollar_amount):
    cursor = db_connection.cursor()
    cursor.execute("INSERT INTO deposits_info (id, telegram_tag, date, user_rubles_deposit, dollar_price, "
                   "dollar_amount) VALUES (?, ?, ?, ?, ?, ?)",
                   (id, telegram_tag, date, user_rubles_deposit, dollar_price, dollar_amount))
    db_connection.commit()


def fetch_max_id(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("SELECT MAX(id) FROM deposits_info")

    max_id = cursor.fetchone()

    return max_id
