from tg_bot.bot import TradingStatBot
from multiprocessing import Process
from data_scraping import data_scrapper
from database.database import Database
from config.db_config import DB_CONFIG


def main():
    db = Database(DB_CONFIG['name'])
    tgBot = TradingStatBot(db).bot
    scrapProcess = Process(target=data_scrapper.scrapDataProcess, args=(db,))
    scrapProcess.start()

    tgBot.polling(none_stop=True, interval=0)


if __name__ == "__main__":
    main()
