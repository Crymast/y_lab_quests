from typing import List

from fastapi import FastAPI

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
import os

from create_table_in_db import create_tables
from models import *

load_dotenv()

app = FastAPI(
    title='Menu app'
)

metadata = MetaData()
engine = create_engine(f"postgresql+psycopg2://"
                       f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
                       f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")
Session = sessionmaker(bind=engine)
session = Session()


# @app.post('/api/v1/menus')
# def add_menu(title: str, description: str):
#     menu = Menu(title=title, description=description)
#     session.add(menu)
#     session.commit()
#     return {
#         "id": menu.menu_uuid,
#         "title": menu.title,
#         "description": menu.description,
#         "submenus_count": 0,
#         "dishes_count": 0
#     }

@app.post('/api/v1/menus', response_model=MenuResponce)
def add_menu(menu: MenuBase):
    menu_item = Menu(
        title=menu.title,
        description=menu.description
    )
    session.add(menu_item)
    session.commit()
    menu_responce = MenuResponce(
        id=menu_item.menu_uuid,
        title=menu_item.title,
        description=menu_item.description,
        submenus_count=0,
        dishes_count=0
    )
    return menu_responce
