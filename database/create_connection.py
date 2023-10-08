import sqlite3

from config.storage_config import STORAGE_CONFIG


def create_db_connection():
    return sqlite3.connect(STORAGE_CONFIG['name'], check_same_thread=False)
