import uuid

from pydantic import BaseModel, Field
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, ForeignKey, String, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MenuBase(BaseModel):
    title: str = Field(max_length=128)
    description: str


class Menu(Base):

    __tablename__ = 'menu'

    menu_uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(128), comment='Наименование меню', nullable=False)
    description = Column(Text, comment='Описание меню', nullable=False)

    def __repr__(self):
        return f'{self.menu_uuid} {self.title} {self.description}'


class MenuResponce(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    submenus_count: int
    dishes_count: int


class Submenu(Base):

    __tablename__ = 'submenu'

    submenu_uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(128), comment='Наименование подменю', nullable=False)
    description = Column(Text, comment='Описание подменю', nullable=False)
    menu_uuid = Column(UUID,  ForeignKey('menu.menu_uuid'), comment='Меню', nullable=False)
    menu = relationship('Menu', backref='submenu_menu', lazy='subquery')

    def __repr__(self):
        return f'{self.submenu_uuid} {self.title} {self.description} {self.menu_uuid}'


class Dish(Base):

    __tablename__ = 'dish'

    dish_uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(128), comment='Наименование блюда', nullable=False)
    description = Column(Text, comment='Описание блюда', nullable=False)
    price = Column(Float(precision=2), comment='Цена блюда', nullable=False)
    submenu_uuid = Column(UUID,  ForeignKey('submenu.submenu_uuid'), comment='Подменю', nullable=False)
    submenu = relationship('Submenu', backref='dish_submenu', lazy='subquery')

    def __repr__(self):
        return f'{self.dish_uuid} {self.title} {self.description} {self.price} {self.submenu_uuid}'