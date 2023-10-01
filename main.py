from tg_bot.bot import TradingStatBot
from multiprocessing import Process
from data_scraping import data_scrapper
from database.database import Database
from config.storage_config import STORAGE_CONFIG


def main():
    db = Database(STORAGE_CONFIG['name'])
    tg_bot = TradingStatBot(db).bot
    scrap_process = Process(target=data_scrapper.scrap_data_process)
    scrap_process.start()

    tg_bot.polling(none_stop=True, interval=0)


if __name__ == "__main__":
    main()
