from database.create_connection import create_db_connection
from tg_bot.bot import TradingStatBot
from multiprocessing import Process
from data_scraping import data_scrapper


def main():
    db_connection = create_db_connection()
    tg_bot = TradingStatBot(db_connection).bot
    scrap_process = Process(target=data_scrapper.scrap_data_process)
    scrap_process.start()

    tg_bot.polling(none_stop=True, interval=0)


if __name__ == "__main__":
    main()
