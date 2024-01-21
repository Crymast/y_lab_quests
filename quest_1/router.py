import uuid

from fastapi import APIRouter, Depends, Response
from fastapi.responses import RedirectResponse
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database import get_async_session

from models.models import menu
from models.schemas import MenuCreate, MenuEdit

router_menu = APIRouter(
    prefix='/api/v1/menus',
    tags=["Menu"]
)


@router_menu.get("/")
async def get_menu(session: AsyncSession = Depends(get_async_session)):
    query = select(menu)
    query_result = await session.execute(query)
    result = []
    for i in query_result:
        result.append(
            {
                "id": i[0],
                "title": i[1],
                "description": i[2],
                "submenus_count": i[3],
                "dishes_count": i[4]
            }
        )
    return result


@router_menu.get("/{api_test_menu_id}")
async def get_menu_id(api_test_menu_id, session: AsyncSession = Depends(get_async_session)):
    query = select(menu).where(menu.c.menu_uuid==api_test_menu_id)
    try:
        result = await session.execute(query)
        result = result.all()[0]
        return {
                    "id": result[0],
                    "title": result[1],
                    "description": result[2],
                    "submenus_count": result[3],
                    "dishes_count": result[4]
                }
    except:
        return {
            "detail": "menu not found"
        }



@router_menu.post("/", status_code=201)
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

@router_menu.patch("/{api_test_menu_id}")
async def path_menu_id(api_test_menu_id, item: MenuEdit, session: AsyncSession = Depends(get_async_session)):
    print(item.title, item.description)
    stmt = (update(menu).where(menu.c.menu_uuid==api_test_menu_id)
            .values(title=item.title, description=item.description))
    try:
        result = await session.execute(stmt)
        await session.commit()
        # result = result.fetchone()
        print(result)
        return {
            "detail": "hello"
        }
    except:
        return {
            "detail": "menu not found"
        }