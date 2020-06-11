import os
from models import Base, engine

basedir = os.path.abspath(os.path.dirname(__file__))
uri = 'sqlite:///' + os.path.join(basedir, 'base.db')


Base.metadata.create_all(engine)