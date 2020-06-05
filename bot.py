import threading
import telegram
from telegram.ext import Updater
from settings import TOKEN, GROUP_ID, CHECK_PER_TIME
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
    # bot = telegram.Bot(token=TOKEN, request=proxy)
    # monitor_matches_tread = threading.Thread(target=monitor_matches, args=[bot])
    # monitor_matches_tread.start()
    bot = Updater(TOKEN, use_context=True, request_kwargs=PROXY)
    matches_info = bot.job_queue
    matches_info.run_repeating(monitor_matches, interval=10, first=0)
    bot.start_polling()
