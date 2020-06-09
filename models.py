from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


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
