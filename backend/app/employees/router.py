from fastapi import APIRouter, Depends, HTTPException
from app.employees.models import Employee
from app.database import async_session_maker
from sqlalchemy import select
from app.employees.dao import EmployeeDAO
from app.employees.rb import RBEmp
from app.employees.schemas import EmployeeSchema, EmployeeCreateSchema, EmployeeUpdateSchema
from typing import List

router_employees = APIRouter(prefix = '/employees', tags = ['Работа со студентами'])

@router_employees.get("/", summary = 'Получить всех сотрудников')
async def get_all_employees(request_body: RBEmp = Depends()):
    return await EmployeeDAO.find_all(**request_body.to_dict())   

@router_employees.get("/{employee_id}", summary = 'Получить сотрудника по ID')
async def get_employee_by_id(employee_id: int) -> EmployeeSchema | dict:
    employee = await EmployeeDAO.find_full_data(employee_id) 
    if not employee:
        return {"error": "Сотрудник c ID " + str(employee_id) + " не найден"}
    return employee

@router_employees.get("/by_filter", summary = 'Получить сотрудника по фильтру')
async def get_employee_by_filter(request_body: RBEmp = Depends()) -> EmployeeSchema | dict:
    employee = await EmployeeDAO.find_one_or_none(**request_body.to_dict())
    if not employee:
        return {"error": "Сотрудник не найден"}
    return employee

@router_employees.post("/", summary = 'Создать нового сотрудника')
async def create_employee(employee_data: EmployeeCreateSchema):
    async with async_session_maker() as session:
        new_employee = Employee(
            name=employee_data.name,
            surname=employee_data.surname,
            role=employee_data.role.value,
            os=employee_data.os.value,
            online=employee_data.online,
            activity_now=employee_data.activity_now
        )
        session.add(new_employee)
        await session.commit()
        await session.refresh(new_employee)
        return new_employee

@router_employees.put("/{employee_id}", summary = 'Обновить сотрудника')
async def update_employee(employee_id: int, employee_data: EmployeeUpdateSchema):
    async with async_session_maker() as session:
        employee = await session.get(Employee, employee_id)
        if not employee:
            raise HTTPException(status_code=404, detail=f"Сотрудник с ID {employee_id} не найден")
        
        update_data = employee_data.model_dump(exclude_unset=True)
        
        # Обрабатываем enum значения
        if 'role' in update_data:
            update_data['role'] = update_data['role'].value
        if 'os' in update_data:
            update_data['os'] = update_data['os'].value
            
        for field, value in update_data.items():
            setattr(employee, field, value)
        
        await session.commit()
        await session.refresh(employee)
        return employee

@router_employees.delete("/{employee_id}", summary = 'Удалить сотрудника')
async def delete_employee(employee_id: int):
    async with async_session_maker() as session:
        employee = await session.get(Employee, employee_id)
        if not employee:
            raise HTTPException(status_code=404, detail=f"Сотрудник с ID {employee_id} не найден")
        
        await session.delete(employee)
        await session.commit()
        return {"message": f"Сотрудник с ID {employee_id} удален"}

@router_employees.post("/{employee_id}/assign_activities", summary = 'Назначить активности сотруднику')
async def assign_activities_to_employee(employee_id: int, activity_ids: List[int]):
    try:
        employee = await EmployeeDAO.assign_activities_to_employee(employee_id, activity_ids)
        return {"message": f"Активности {activity_ids} назначены сотруднику {employee_id}", "employee": employee}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router_employees.post("/{employee_id}/add_activity/{activity_id}", summary = 'Добавить активность сотруднику')
async def add_activity_to_employee(employee_id: int, activity_id: int):
    try:
        employee = await EmployeeDAO.add_activity_to_employee(employee_id, activity_id)
        return {"message": f"Активность {activity_id} добавлена сотруднику {employee_id}", "employee": employee}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))








