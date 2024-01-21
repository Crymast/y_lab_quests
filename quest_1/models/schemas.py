import uuid

from pydantic import BaseModel


class MenuCreate(BaseModel):
    title: str
    description: str
    submenus_count: int = 0
    dishes_count: int = 0


class MenuEdit(BaseModel):
    title: str
    description: str
