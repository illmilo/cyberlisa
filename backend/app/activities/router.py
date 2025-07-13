from fastapi import APIRouter, Depends, HTTPException
from app.activities.models import Activity
from app.activities.dao import ActivityDAO
from app.activities.schemas import ActivitySchema, ActivityCreateSchema, ActivityUpdateSchema
from app.database import async_session_maker
from sqlalchemy import select

router_activities = APIRouter(prefix='/activities', tags=['Работа с активностями'])


@router_activities.get("/", summary='Получить все активности')
async def get_all_activities():
    return await ActivityDAO.find_all()


@router_activities.get("/{activity_id}", summary='Получить активность по ID')
async def get_activity_by_id(activity_id: int):
    activity = await ActivityDAO.find_full_data(activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail=f"Активность с ID {activity_id} не найдена")
    return activity





@router_activities.post("/", summary='Создать новую активность')
async def create_activity(activity_data: ActivityCreateSchema):
    async with async_session_maker() as session:
        new_activity = Activity(
            name=activity_data.name,
            url=activity_data.url,
            description=activity_data.description,
            os=activity_data.os.value
        )
        session.add(new_activity)
        await session.commit()
        await session.refresh(new_activity)
        return new_activity


@router_activities.put("/{activity_id}", summary='Обновить активность')
async def update_activity(activity_id: int, activity_data: ActivityUpdateSchema):
    async with async_session_maker() as session:
        activity = await session.get(Activity, activity_id)
        if not activity:
            raise HTTPException(status_code=404, detail=f"Активность с ID {activity_id} не найдена")
        
        update_data = activity_data.model_dump(exclude_unset=True)
        if 'os' in update_data:
            update_data['os'] = update_data['os'].value
            
        for field, value in update_data.items():
            setattr(activity, field, value)
        
        await session.commit()
        await session.refresh(activity)
        return activity


@router_activities.delete("/{activity_id}", summary='Удалить активность')
async def delete_activity(activity_id: int):
    async with async_session_maker() as session:
        activity = await session.get(Activity, activity_id)
        if not activity:
            raise HTTPException(status_code=404, detail=f"Активность с ID {activity_id} не найдена")
        
        await session.delete(activity)
        await session.commit()
        return {"message": f"Активность с ID {activity_id} удалена"} 