from fastapi import APIRouter, HTTPException
from app.roles.dao import RoleDAO
from app.roles.schemas import RoleSchema, RoleCreateSchema, RoleUpdateSchema, RoleSetActivitiesSchema, RoleNameSchema
from typing import List

router_roles = APIRouter(prefix='/roles', tags=['Роли'])

@router_roles.get('/', response_model=List[RoleSchema])
async def get_all_roles() :
    return await RoleDAO.get_all()

@router_roles.get('/{role_id}', response_model=RoleSchema)
async def get_role(role_id: int):
    role = await RoleDAO.get_by_id(role_id)
    if not role:
        raise HTTPException(status_code=404, detail='Роль не найдена')
    return role

@router_roles.post('/', response_model=RoleSchema)
async def create_role(role: RoleCreateSchema):
    return await RoleDAO.create(name=role.name)

@router_roles.put('/{role_id}', response_model=RoleSchema)
async def update_role(role_id: int, role_data: RoleUpdateSchema):
    role = await RoleDAO.update(role_id, name=role_data.name)
    if not role:
        raise HTTPException(status_code=404, detail='Роль не найдена')
    return role

@router_roles.delete('/{role_id}')
async def delete_role(role_id: int):
    success = await RoleDAO.delete(role_id)
    if not success:
        raise HTTPException(status_code=404, detail='Роль не найдена')
    return {"message": "Роль удалена"}

@router_roles.post('/{role_id}/set_activities', response_model=RoleSchema)
async def set_activities(role_id: int, data: RoleSetActivitiesSchema):
    role = await RoleDAO.set_activities(role_id, data.activity_ids)
    if not role:
        raise HTTPException(status_code=404, detail='Роль не найдена')
    return role
