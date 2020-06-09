import os
from sqlalchemy import create_engine
from models import Base, Match

basedir = os.path.abspath(os.path.dirname(__file__))
uri = 'sqlite:///' + os.path.join(basedir, 'base.db')


engine = create_engine(uri)


if __name__ == '__main__':
    Base.metadata.create_all(engine)