from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from backend.app.employees.models import Employee
from backend.app.activities.models import Activity
from backend.app.database import async_session_maker
from backend.app.dao.base import BaseDAO


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

            employee_data = employee_info.to_dict()

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

            employee_data['activities'] = [activity.to_dict() for activity in (employee_info.activities or [])]

            return employee_data

    @classmethod
    async def assign_activities_to_employee(cls, employee_id: int, activity_ids: list[int]):
        """Назначить активности сотруднику"""
        async with async_session_maker() as session:
            query_employee = select(Employee).options(selectinload(Employee.activities)).filter_by(id=employee_id)
            result_employee = await session.execute(query_employee)
            employee = result_employee.scalar_one_or_none()
            
            if not employee:
                raise ValueError(f"Сотрудник с ID {employee_id} не найден")
            
            query_activities = select(Activity).filter(Activity.id.in_(activity_ids))
            result_activities = await session.execute(query_activities)
            activities = result_activities.scalars().all()
            
            employee.activities.clear()
            employee.activities.extend(activities)
            
            await session.commit()
            await session.refresh(employee)
            
            return employee

    @classmethod
    async def add_activity_to_employee(cls, employee_id: int, activity_id: int):
        """Добавить одну активность сотруднику"""
        async with async_session_maker() as session:
            query_employee = select(Employee).options(selectinload(Employee.activities)).filter_by(id=employee_id)
            result_employee = await session.execute(query_employee)
            employee = result_employee.scalar_one_or_none()
            
            if not employee:
                raise ValueError(f"Сотрудник с ID {employee_id} не найден")
            
            activity = await session.get(Activity, activity_id)
            if not activity:
                raise ValueError(f"Активность с ID {activity_id} не найдена")
            
            if activity not in employee.activities:
                employee.activities.append(activity)
            
            await session.commit()
            await session.refresh(employee)
            
            return employee

    @classmethod
    async def get_agent_config_from_db(cls, employee_id: int):
        async with async_session_maker() as session:
            stmt = (
                select(cls.model)
                .options(selectinload(cls.model.activities))
                .filter_by(id=employee_id)
            )
            result = await session.execute(stmt)
            employee = result.scalar_one_or_none()
            if not employee:
                return None
            config = {
                "employee_id": employee.id,
                "role": employee.role,
                "work_start_time": employee.work_start_time.isoformat() if employee.work_start_time else None,
                "work_end_time": employee.work_end_time.isoformat() if employee.work_end_time else None,
                "activity_rate": employee.activity_rate,
                "actions": [
                    {"id": act.id, "name": act.name, "url": act.url, "description": act.description, "os": act.os}
                    for act in (employee.activities or [])
                ]
            }
            return config