import threading
from telegram.ext import Updater, MessageHandler, Filters
from settings import MSG_TO_CHAT_TIMEOUT
from token_ import TOKEN
from utils import monitor_matches, run_command, check_and_add_to_db

import logging

def main():
    pass


PROXY = {
    'proxy_url': 'socks5://t3.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}
}



if __name__ == '__main__':
    bot = Updater(TOKEN, use_context=True)
    dp = bot.dispatcher
    matches_info = bot.job_queue
    matches_info.run_repeating(monitor_matches, interval=MSG_TO_CHAT_TIMEOUT, first=0)
    dp.add_handler(MessageHandler(Filters.text, run_command))
    thread = threading.Thread(target=check_and_add_to_db)
    thread.start()

    bot.start_polling()
