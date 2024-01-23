import uuid

from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, delete
from sqlalchemy import update
from models.models import metadata, menu, submenu, dish

from models.schemas import MenuCreate, MenuResponse, SubmenuCreate, SubmenuResponse, DishCreate, DishResponse, \
    MenuUpdate
from sqlalchemy import func

from database import get_async_session

router = APIRouter(prefix='/api/v1')


# Menu CRUD Operations
@router.get("/menus/", response_model=list[MenuResponse])
async def get_menu(session: AsyncSession = Depends(get_async_session)):
    stmt = select(
        menu.c.menu_uuid,
        menu.c.title,
        menu.c.description
    )
    result = await session.execute(stmt)
    menu_list = result.fetchall()

    async def submenus_count(menu_uuid):
        dishes_submenus_count = 0
        stmt_def_count = select(submenu).where(menu_uuid==submenu.c.menu_uuid)
        result_def_count = await session.execute(stmt_def_count)
        result_def_count_fetchall = result_def_count.fetchall()
        for i in result_def_count_fetchall:
            stmt_def_count_dish = select(dish).where(i[0]==dish.c.submenu_uuid)
            result_def_count_dish = await session.execute(stmt_def_count_dish)
            result_def_count_dish_fetchall = result_def_count_dish.fetchall()
            dishes_submenus_count += len(result_def_count_dish_fetchall)
        return len(result_def_count_fetchall), dishes_submenus_count

    result = []

    for m in menu_list:
        submenus_count_res, dishes_count_res = await submenus_count(m.menu_uuid)
        result.append(
            {
                'id': m.menu_uuid,
                'title': m.title,
                'description': m.description,
                'submenus_count': submenus_count_res,
                'dishes_count': dishes_count_res
            }
        )
    return result


@router.get("/menus/{menu_id}")
async def get_menu(menu_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    stmt = select(menu).where(menu.c.menu_uuid == menu_id)
    result = await session.execute(stmt)
    menu_item = result.fetchall()
    if not menu_item:
        raise HTTPException(status_code=404,
                            detail={
                                "detail": "menu not found"
                            })


    async def submenus_count(menu_uuid):
        dishes_submenus_count = 0
        stmt_def_count = select(submenu).where(menu_uuid==submenu.c.menu_uuid)
        result_def_count = await session.execute(stmt_def_count)
        result_def_count_fetchall = result_def_count.fetchall()
        for i in result_def_count_fetchall:
            stmt_def_count_dish = select(dish).where(i[0]==dish.c.submenu_uuid)
            result_def_count_dish = await session.execute(stmt_def_count_dish)
            result_def_count_dish_fetchall = result_def_count_dish.fetchall()
            dishes_submenus_count += len(result_def_count_dish_fetchall)
        return len(result_def_count_fetchall), dishes_submenus_count
    a, b = await submenus_count(menu_item[0][0])
    return {
                'id': menu_item[0][0],
                'title': menu_item[0][1],
                'description': menu_item[0][2],
                'submenus_count': a,
                'dishes_count': b
            }


@router.post("/menus/", response_model=MenuResponse, status_code=201)
async def create_menu(menu_data: MenuCreate, session: AsyncSession = Depends(get_async_session)):
    new_menu = menu.insert().values(**menu_data.dict())
    result = await session.execute(new_menu)
    await session.commit()
    menu_id = result.inserted_primary_key[0]
    return {
        **menu_data.model_dump(),
        "id": menu_id,
        "submenus_count": 0,
        "dishes_count": 0
    }


@router.patch("/menus/{menu_id}")
async def update_menu(menu_id: uuid.UUID, menu_data: MenuUpdate, session: AsyncSession = Depends(get_async_session)):
    stmt = (
        update(menu)
        .where(menu.c.menu_uuid == menu_id)
        .values(**menu_data.dict(exclude_unset=True))
        .returning(menu)
    )
    result = await session.execute(stmt)
    updated_menu = result.fetchone()
    await session.commit()
    if not updated_menu:
        raise HTTPException(status_code=404,
                            detail={
                                "detail": "menu not found"
                            })

    async def submenus_count(menu_uuid):
        dishes_submenus_count = 0
        stmt_def_count = select(submenu).where(menu_uuid==submenu.c.menu_uuid)
        result_def_count = await session.execute(stmt_def_count)
        result_def_count_fetchall = result_def_count.fetchall()
        for i in result_def_count_fetchall:
            stmt_def_count_dish = select(dish).where(i[0]==dish.c.submenu_uuid)
            result_def_count_dish = await session.execute(stmt_def_count_dish)
            result_def_count_dish_fetchall = result_def_count_dish.fetchall()
            dishes_submenus_count += len(result_def_count_dish_fetchall)
        return len(result_def_count_fetchall), dishes_submenus_count
    a, b = await submenus_count(updated_menu[0])
    res = {
    "id": updated_menu[0],
    "title": updated_menu[1],
    "description": updated_menu[2],
    "submenus_count": a,
    "dishes_count": b
    }
    return res


@router.delete("/menus/{menu_id}")
async def delete_menu(menu_id: str, session: AsyncSession = Depends(get_async_session)):
    query = delete(menu).where(menu.c.menu_uuid == menu_id)
    await session.execute(query)
    await session.commit()
    return {
        "status": True,
        "message": "The menu has been deleted"
    }


# Submenu CRUD Operations
@router.get("/submenus/", response_model=list[SubmenuResponse])
async def get_submenus(session: AsyncSession = Depends(get_async_session)):
    # Join submenu with dish, group by submenu fields, and count dish
    stmt = select([
        submenu.c.submenu_uuid,
        submenu.c.title,
        submenu.c.description,
        func.count(dish.c.dish_uuid).label('dishes_count')
    ]).select_from(submenu.outerjoin(dish)).group_by(submenu.c.submenu_uuid, submenu.c.title, submenu.c.description)
    result = await session.execute(stmt)
    submenu_list = result.fetchall()
    return [{
        'id': s.submenu_uuid,
        'title': s.title,
        'description': s.description,
        'dishes_count': s.dishes_count
    } for s in submenu_list]

@router.post("/submenus/", response_model=SubmenuResponse)
async def create_submenu(submenu_data: SubmenuCreate, session: AsyncSession = Depends(get_async_session)):
    new_submenu = submenu.insert().values(**submenu_data.dict())
    result = await session.execute(new_submenu)
    await session.commit()
    submenu_id = result.inserted_primary_key[0]
    return {**submenu_data.dict(), "id": submenu_id, "dishes_count": 0}

@router.delete("/submenus/{submenu_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_submenu(submenu_id: str, session: AsyncSession = Depends(get_async_session)):
    query = delete(submenu).where(submenu.c.submenu_uuid == submenu_id)
    await session.execute(query)
    await session.commit()
    return {"detail": "Submenu deleted"}

# Dish CRUD Operations
@router.get("/dishes/", response_model=list[DishResponse])
async def get_dishes(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(dish))
    dish_list = result.fetchall()
    return [DishResponse(
                id=d.dish_uuid,
                title=d.title,
                description=d.description,
                price=d.price
            ) for d in dish_list]
@router.post("/dishes/", response_model=DishResponse)
async def create_dish(dish_data: DishCreate, session: AsyncSession = Depends(get_async_session)):
    new_dish = dish.insert().values(**dish_data.dict())
    result = await session.execute(new_dish)
    await session.commit()
    dish_id = result.inserted_primary_key[0]
    return {**dish_data.dict(), "id": dish_id}

@router.delete("/dishes/{dish_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dish(dish_id: str, session: AsyncSession = Depends(get_async_session)):
    query = delete(dish).where(dish.c.dish_uuid == dish_id)
    await session.execute(query)
    await session.commit()
    return {"detail": "Dish deleted"}
