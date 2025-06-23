from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from app.employees.models import Employee
from app.activities.models import Activity
from app.database import async_session_maker
from app.dao.base import BaseDAO


class EmployeeDAO(BaseDAO):
    model = Employee

    @classmethod
    async def find_full_data(cls, employee_id: int):
        async with async_session_maker() as session:
            stmt = (
                select(cls.model)
                .options(
                    selectinload(cls.model.activities).selectinload(Activity.employees)
                )
                .filter_by(id=employee_id)
            )
            result_employee = await session.execute(stmt)
            employee_info = result_employee.unique().scalar_one_or_none()

            if not employee_info:
                return None

            # Сериализация до выхода из сессии
            employee_data = employee_info.to_dict()

            # Проверяем, есть ли активность сейчас
            if employee_info.activity_now:
                query_activity = select(Activity).filter_by(id=employee_info.activity_now)
                result_activity = await session.execute(query_activity)
                activity_info = result_activity.scalar_one_or_none()
                if activity_info:
                    employee_data['activity_now'] = activity_info.to_dict()
                else:
                    employee_data['activity_now'] = None
            else:
                employee_data['activity_now'] = None

            # Безопасная обработка activities
            employee_data['activities'] = [activity.to_dict() for activity in (employee_info.activities or [])]

            return employee_data

    @classmethod
    async def assign_activities_to_employee(cls, employee_id: int, activity_ids: list[int]):
        """Назначить активности сотруднику"""
        async with async_session_maker() as session:
            # Получаем сотрудника с загруженными активностями
            query_employee = select(Employee).options(selectinload(Employee.activities)).filter_by(id=employee_id)
            result_employee = await session.execute(query_employee)
            employee = result_employee.scalar_one_or_none()
            
            if not employee:
                raise ValueError(f"Сотрудник с ID {employee_id} не найден")
            
            # Получаем активности
            query_activities = select(Activity).filter(Activity.id.in_(activity_ids))
            result_activities = await session.execute(query_activities)
            activities = result_activities.scalars().all()
            
            # Очищаем существующие активности и добавляем новые
            employee.activities.clear()
            employee.activities.extend(activities)
            
            await session.commit()
            await session.refresh(employee)
            
            return employee

    @classmethod
    async def add_activity_to_employee(cls, employee_id: int, activity_id: int):
        """Добавить одну активность сотруднику"""
        async with async_session_maker() as session:
            # Получаем сотрудника с загруженными активностями
            query_employee = select(Employee).options(selectinload(Employee.activities)).filter_by(id=employee_id)
            result_employee = await session.execute(query_employee)
            employee = result_employee.scalar_one_or_none()
            
            if not employee:
                raise ValueError(f"Сотрудник с ID {employee_id} не найден")
            
            # Получаем активность
            activity = await session.get(Activity, activity_id)
            if not activity:
                raise ValueError(f"Активность с ID {activity_id} не найдена")
            
            # Проверяем, нет ли уже такой активности
            if activity not in employee.activities:
                employee.activities.append(activity)
            
            await session.commit()
            await session.refresh(employee)
            
            return employee