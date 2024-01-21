

from fastapi import APIRouter, Depends, Response
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session

from models.models import menu
from models.schemas import MenuCreate

router_menu = APIRouter(
    prefix='/api/v1/menus',
    tags=["Menu"]
)


@router_menu.get("/")
async def get_menu(session: AsyncSession = Depends(get_async_session)):
    query = select(menu)
    result = await session.execute(query)
    return result.all()


@router_menu.post("/")
async def add_menu(new_menu: MenuCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(menu).values(**new_menu.dict())
    result = await session.execute(stmt)
    await session.commit()
    uuiv_value = result.inserted_primary_key
    uuiv_value = str(uuiv_value[0])
    return {
        "id": uuiv_value,
        "title": new_menu.title,
        "description": new_menu.description,
        "submenus_count": 0,
        "dishes_count": 0
    }
