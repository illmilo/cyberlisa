from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.activities.models import Activity
from app.database import async_session_maker
from app.dao.base import BaseDAO


class ActivityDAO(BaseDAO):
    model = Activity

    @classmethod
    async def find_full_data(cls, activity_id: int):
        async with async_session_maker() as session:
            query_activity = select(cls.model).options(joinedload(cls.model.employees)).filter_by(id=activity_id)
            result_activity = await session.execute(query_activity)
            activity_info = result_activity.scalar_one_or_none()

            if not activity_info:
                return None

            activity_data = activity_info.to_dict()
            
            # Проверяем, есть ли активность
            if activity_info.activity_now:
                query_activity = select(Activity).filter_by(id=activity_info.activity_now)
                result_activity = await session.execute(query_activity)
                activity_info = result_activity.scalar_one_or_none()
                
                if activity_info:
                    activity_data['activity_now'] = activity_info.to_dict()
                else:
                    activity_data['activity_now'] = None
            else:
                activity_data['activity_now'] = None
            
            # Безопасная обработка activities
            activity_data['employees'] = [employee.to_dict() for employee in (activity_info.employees or list())]  

            return activity_data

    @classmethod
    async def find_with_employees(cls, activity_id: int):
        """Получить активность со связанными сотрудниками"""
        async with async_session_maker() as session:
            query_activity = select(cls.model).options(joinedload(cls.model.employees)).filter_by(id=activity_id)
            result_activity = await session.execute(query_activity)
            activity_info = result_activity.scalar_one_or_none()

            if not activity_info:
                return None

            activity_data = activity_info.to_dict()
            activity_data['employees'] = [employee.to_dict() for employee in activity_info.employees] if activity_info.employees else list()

            return activity_data 