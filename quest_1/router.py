import uuid

from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, delete
from sqlalchemy import update
from models.models import metadata, menu, submenu, dish

from models.schemas import MenuCreate, MenuResponse, SubmenuCreate, SubmenuResponse, DishCreate, DishResponse
from sqlalchemy import func

from database import get_async_session

router = APIRouter(prefix='/api/v1')


@router.get("/test")
async def get_menu(session: AsyncSession = Depends(get_async_session)):
    stmt = select(
        menu.c.menu_uuid,
        menu.c.title,
        menu.c.description
    )
    result = await session.execute(stmt)
    menu_list = result.fetchall()

    test_uuid = uuid.UUID("399b2aed-864f-4b57-bbfd-5272b7aa8b7d")
    test_stmt = select(submenu).where(menu.c.menu_uuid==submenu.c.menu_uuid)
    test_result = await session.execute(test_stmt)

    async def submenus_count(menu_uuid):
        stmt_def_count = select(submenu).where(menu_uuid==submenu.c.menu_uuid)
        result_def_count = await session.execute(stmt_def_count)
        # print(submenu.c.submenu_uuid)
        return len(result_def_count.fetchall())


    return [{
        'id': m.menu_uuid,
        'title': m.title,
        'description': m.description,
        'submenus_count': await submenus_count(m.menu_uuid),
        'dishes_count': 0
    } for m in menu_list]


# Menu CRUD Operations
@router.get("/menus/", response_model=list[MenuResponse])
async def get_menus(session: AsyncSession = Depends(get_async_session)):
    subq = select([
        submenu.c.menu_uuid,
        func.count(submenu.c.submenu_uuid.distinct()).label('submenus_count'),
        func.count(dish.c.dish_uuid.distinct()).label('dishes_count')
    ]).select_from(submenu.outerjoin(dish, submenu.c.submenu_uuid == dish.c.submenu_uuid)
                   ).group_by(submenu.c.menu_uuid
                              ).subquery()

    stmt = select([
        menu.c.menu_uuid,
        menu.c.title,
        menu.c.description,
        subq.c.submenus_count,
        subq.c.dishes_count
    ]).select_from(menu.join(subq, menu.c.menu_uuid == subq.c.menu_uuid))

    result = await session.execute(stmt)
    menu_list = result.fetchall()
    return [{
        'id': m.menu_uuid,
        'title': m.title,
        'description': m.description,
        'submenus_count': m.submenus_count if m.submenus_count else 0,  # Ensure a default value if None
        'dishes_count': m.dishes_count if m.dishes_count else 0  # Ensure a default value if None
    } for m in menu_list]


@router.get("/menus/{menu_id}", response_model=MenuResponse)
async def get_menu(menu_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    stmt = select([menu]).where(menu.c.menu_uuid == menu_id)
    result = await session.execute(stmt)
    menu_item = result.fetchone()
    if not menu_item:
        raise HTTPException(status_code=404, detail="Menu not found")
    return menu_item


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
