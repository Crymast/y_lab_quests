import uuid

from pydantic import BaseModel


class MenuCreate(BaseModel):
    title: str
    description: str


class MenuResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    submenus_count: int
    dishes_count: int