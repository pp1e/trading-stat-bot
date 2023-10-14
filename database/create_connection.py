import sqlite3

from config.storage_config import STORAGE_CONFIG
from database import deposit_info_table
from database import users_rights_table
from database import weeks_stats_table


def create_db_connection():
    db_connection = sqlite3.connect(STORAGE_CONFIG['name'], check_same_thread=False)
    deposit_info_table.create_table(db_connection)
    users_rights_table.create_table(db_connection)
    weeks_stats_table.create_table(db_connection)
    return db_connection
