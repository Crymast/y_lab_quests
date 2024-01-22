import uuid

from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, UUID, Text, Float

metadata = MetaData()

menu = Table(
    "menu",
    metadata,
    Column("menu_uuid", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("title", String(128), nullable=False),
    Column("description", Text)
)

submenu = Table(
    "submenu",
    metadata,
    Column("submenu_uuid", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("title", String(128), nullable=False),
    Column("description", Text),
    Column("menu_uuid", UUID,  ForeignKey('menu.menu_uuid', ondelete='CASCADE'), nullable=False)
)

dish = Table(
    "dish",
    metadata,
    Column("dish_uuid", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("title", String(128), nullable=False),
    Column("description", Text),
    Column("price", Float(precision=2), nullable=False),
    Column("submenu_uuid", UUID,  ForeignKey('submenu.submenu_uuid', ondelete='CASCADE'), nullable=False)
)
