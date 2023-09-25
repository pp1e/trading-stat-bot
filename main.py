from tg_bot.bot import TradingStatBot
from multiprocessing import Process
from data_scraping import data_scrapper
from database.database import Database
from config.storage_config import STORAGE_CONFIG


def main():
    db = Database(STORAGE_CONFIG['name'])
    tgBot = TradingStatBot(db).bot
    scrapProcess = Process(target=data_scrapper.scrapDataProcess)
    scrapProcess.start()

    tgBot.polling(none_stop=True, interval=0)


if __name__ == "__main__":
    main()
