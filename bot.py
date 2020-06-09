import threading
from telegram.ext import Updater, MessageHandler, Filters
from settings import INTERVAL
from token_ import API_KEY
from utils import monitor_matches, run_command, check_and_add_to_db


def main():
    pass


PROXY = {
    'proxy_url': 'socks5h://t3.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}
}



if __name__ == '__main__':
    bot = Updater(API_KEY, use_context=True)
    dp = bot.dispatcher
    matches_info = bot.job_queue
    matches_info.run_repeating(monitor_matches, interval=INTERVAL, first=0)
    dp.add_handler(MessageHandler(Filters.text, run_command))
    thread = threading.Thread(target=check_and_add_to_db)
    thread.start()
    bot.start_polling()
