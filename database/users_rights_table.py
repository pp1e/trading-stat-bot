
def create_table(db_connection):
    cursor = db_connection.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE TYPE = 'table' AND NAME = 'users_rights';")
    query_result = cursor.fetchone()

    if not query_result:
        cursor.execute('''
            CREATE TABLE users_rights
            (telegram_tag TEXT PRIMARY KEY,
            role TEXT,
            balance REAL)
            ''')

    db_connection.commit()


def fetch_user_role(db_connection, username):
    cursor = db_connection.cursor()

    cursor.execute("SELECT role FROM users_rights WHERE telegram_tag = ?", (username,))
    role = cursor.fetchone()
    return role


def fetch_user_tags(db_connection):
    cursor = db_connection.cursor()

    cursor.execute("SELECT telegram_tag FROM users_rights")
    query_result = cursor.fetchall()
    users = [item[0] for item in query_result]
    return users


def update_balance(db_connection, username_pays, amount):
    cursor = db_connection.cursor()

    cursor.execute("UPDATE users_rights SET balance = balance + ? WHERE telegram_tag = ?",
                   (amount, username_pays))
    db_connection.commit()


def fetch_user_balances(db_connection):
    cursor = db_connection.cursor()

    cursor.execute("SELECT telegram_tag, balance FROM users_rights")
    query_result = cursor.fetchall()

    return query_result
