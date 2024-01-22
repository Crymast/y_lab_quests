import uuid
from pydantic import BaseModel, Field

# Menu Schemas
class MenuBase(BaseModel):
    title: str
    description: str

class MenuCreate(MenuBase):
    pass

class MenuUpdate(BaseModel):
    title: str = None
    description: str = None

class MenuResponse(MenuBase):
    id: uuid.UUID
    submenus_count: int
    dishes_count: int

# Submenu Schemas
class SubmenuBase(BaseModel):
    title: str
    description: str

class SubmenuCreate(SubmenuBase):
    menu_id: uuid.UUID

class SubmenuUpdate(BaseModel):
    title: str = None
    description: str = None

class SubmenuResponse(SubmenuBase):
    id: uuid.UUID
    dishes_count: int

# Dish Schemas
class DishBase(BaseModel):
    title: str
    description: str
    price: float = Field(..., gt=0)

class DishCreate(DishBase):
    submenu_id: uuid.UUID

class DishUpdate(BaseModel):
    title: str = None
    description: str = None
    price: float = None

class DishResponse(DishBase):
    id: uuid.UUID