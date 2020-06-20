import os
from models import Base, engine

basedir = os.path.abspath(os.path.dirname(__file__))


Base.metadata.create_all(engine)