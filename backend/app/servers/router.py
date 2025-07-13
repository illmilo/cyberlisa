from fastapi import APIRouter, Body
from app.servers.dao import ServerDAO
from app.servers.schemas import ServerSchema, ServerCreateSchema, ServerUpdateSchema
from app.employees.schemas import EmployeeSchema, EmployeeSchemaWnoActivities
from typing import List


router_servers = APIRouter(prefix = '/servers', tags = ['Работа с серверами'])

@router_servers.get("/", summary = 'Получить все сервера')
async def get_all_servers() -> List[ServerSchema] | dict:
    servers = await ServerDAO.get_all_servers()
    if not servers:
        return {"error": "Сервера не найдены"}
    return [ServerSchema.model_validate(server) for server in servers]

@router_servers.get("/{server_id}", summary = 'Получить сервер по ID')
async def get_server_by_id(server_id: int) -> ServerSchema | dict:
    server = await ServerDAO.get_server_by_id(server_id)
    if not server:
        return {"error": "Сервер с ID " + str(server_id) + " не найден"}
    return ServerSchema.model_validate(server)

@router_servers.get("/{server_id}/employees", summary = 'Получить агентов сервера по ID')
async def get_server_employees(server_id: int) -> List[EmployeeSchemaWnoActivities] | dict:
    employees = await ServerDAO.get_server_employees(server_id)
    if not employees:
        return {"error": "Агенты не найдены"}
    return [EmployeeSchemaWnoActivities.model_validate(emp) for emp in employees]

@router_servers.post("/", summary = 'Создать сервер')
async def create_server(server_data: ServerCreateSchema = Body(...)):
    await ServerDAO.create_server(server_data.model_dump())
    return {"message": "Сервер успешно создан"}

@router_servers.put("/{server_id}", summary = 'Обновить сервер')
async def update_server(server_id: int, server_data: ServerUpdateSchema = Body(...)):
    await ServerDAO.update_server(server_id, server_data.model_dump(exclude_unset=True))
    return {"message": "Сервер успешно обновлен"}

@router_servers.delete("/{server_id}", summary = 'Удалить сервер')
async def delete_server(server_id: int):
    await ServerDAO.delete_server(server_id)
    return {"message": "Сервер успешно удален"}

@router_servers.post("/{server_id}/employees", summary = 'Добавить агента на сервер')
async def add_employee_to_server(server_id: int, employee_id: int):
    await ServerDAO.add_employee_to_server(server_id, employee_id)
    return {"message": "Агент успешно добавлен на сервер"}

@router_servers.delete("/{server_id}/employees/{employee_id}", summary = 'Удалить агента с сервера')
async def remove_employee_from_server(server_id: int, employee_id: int):
    await ServerDAO.remove_employee_from_server(server_id, employee_id)
    return {"message": "Агент успешно удален с сервера"}
