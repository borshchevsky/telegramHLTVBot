from sqlalchemy import Column, Integer, DateTime, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from settings import DB_URI

Base = declarative_base()
engine = create_engine(DB_URI)


class Match(Base):
    __tablename__ = 'matches'
    id = Column(Integer, primary_key=True)
    team1 = Column(String)
    team2 = Column(String)
    match_time = Column(DateTime)
    best_of = Column(String)
    event = Column(String)
    match_url = Column(String, unique=True)
    twitch = Column(String)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(String, unique=True)
    role = Column(String)
