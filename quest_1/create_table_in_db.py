from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
import os

from models import *

load_dotenv()
metadata = MetaData()
engine = create_engine(f"postgresql+asyncpg://"
                       f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
                       f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")
session = sessionmaker(bind=engine)


def create_tables():
    Base.metadata.create_all(engine)
