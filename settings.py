import os

GROUP_ID = -443926074
TEAM = 'vitality'
MSG_TO_CHAT_TIMEOUT = 10  # раз в сколько времени (в секундах) проверять наличие матчей команды
CHECK_HLTV_TIMEOUT = 1200

basedir = os.path.abspath(os.path.dirname(__file__))
DB_URI = 'sqlite:///' + os.path.join(basedir, 'base.db?check_same_thread=False')
ROLES = {'admin', 'user'}