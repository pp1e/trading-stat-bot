from tg_bot import bot
from multiprocessing import Process
from data_scraping import data_scrapper


def main():
    tgBot = bot.bot

    scrapProcess = Process(target=data_scrapper.scrapDataProcess)
    scrapProcess.start()
    tgBot.polling(none_stop=True, interval=0)


if __name__ == "__main__":
    main()
