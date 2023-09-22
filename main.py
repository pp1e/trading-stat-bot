from tg_bot import bot
from multiprocessing import Process
from data_scraping import data_scrapper
from database import database
from config.db_config import DB_CONFIG


def main():
    data_base = database.Database(DB_CONFIG['name'])
    tgBot = bot.Bot(data_base).bot
    scrapProcess = Process(target=data_scrapper.scrapDataProcess)
    scrapProcess.start()

    tgBot.polling(none_stop=True, interval=0)


if __name__ == "__main__":
    main()
