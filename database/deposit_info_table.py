

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
