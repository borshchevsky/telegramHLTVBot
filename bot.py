import threading
import telegram
from telegram.ext import Updater
from settings import GROUP_ID, INTERVAL
from token import TOKEN
from utils import monitor_matches
import datetime


def main():
    pass


PROXY = {
    'proxy_url': 'socks5://t3.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}
}


proxy = telegram.utils.request.Request(proxy_url='socks5://learn:python@t3.learn.python.ru:1080')

if __name__ == '__main__':
    bot = Updater(TOKEN, use_context=True, request_kwargs=PROXY)
    matches_info = bot.job_queue
    matches_info.run_repeating(monitor_matches, interval=INTERVAL, first=0)
    bot.start_polling()
