import os

GROUP_ID = -443926074
TEAM = 'vitality'
INTERVAL = 1800  # раз в сколько времени (в секундах) проверять наличие матчей команды

basedir = os.path.abspath(os.path.dirname(__file__))
DB_URI = 'sqlite:///' + os.path.join(basedir, 'base.db')
ROLES = {'admin', 'user'}