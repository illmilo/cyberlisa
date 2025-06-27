from app.database import async_session_maker
from app.dao.base import BaseDAO
from app.servers.models import Server
from sqlalchemy import select
from app.employees.models import Employee


class ServerDAO(BaseDAO):
    model = Server

    @classmethod
    async def get_server_by_id(cls, server_id: int):
        async with async_session_maker() as session:
            stmt = select(cls.model).filter_by(id=server_id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()
    
    # @classmethod
    # async def get_server_by_name(cls, server_name: str):
    #     async with async_session_maker() as session:
    #         stmt = select(cls.model).filter_by(name=server_name)
    #         result = await session.execute(stmt)
    #         return result.scalar_one_or_none()
    
    @classmethod
    async def get_all_servers(cls):
        async with async_session_maker() as session:
            stmt = select(cls.model)
            result = await session.execute(stmt)
            return result.scalars().all()
    
    @classmethod
    async def create_server(cls, server_data: dict):
        async with async_session_maker() as session:
            new_server = cls.model(**server_data)
            session.add(new_server)
            await session.commit()
            return True
        
    @classmethod
    async def update_server(cls, server_id: int, server_data: dict):
        async with async_session_maker() as session:
            stmt = select(cls.model).filter_by(id=server_id)
            result = await session.execute(stmt)
            server = result.scalar_one_or_none()
            if server:
                for key, value in server_data.items():
                    setattr(server, key, value)
            await session.commit()
            return True
        
    @classmethod
    async def delete_server(cls, server_id: int):
        async with async_session_maker() as session:
            stmt = select(cls.model).filter_by(id=server_id)
            result = await session.execute(stmt)
            server = result.scalar_one_or_none()
            if server:
                await session.delete(server)
                await session.commit()
                return True
            return False
        
    @classmethod
    async def add_employee_to_server(cls, server_id: int, employee_id: int):
        async with async_session_maker() as session:
            server = await session.get(Server, server_id)
            employee = await session.get(Employee, employee_id)
            if server and employee:
                employee.server_id = server.id
                await session.commit()
                return True
            return False
        
    @classmethod
    async def remove_employee_from_server(cls, server_id: int, employee_id: int):
        async with async_session_maker() as session:
            employee = await session.get(Employee, employee_id)
            if employee and employee.server_id == server_id:
                employee.server_id = None
                await session.commit()
                return True
            return False
        
    @classmethod
    async def get_server_employees(cls, server_id: int):
        async with async_session_maker() as session:
            result = await session.execute(
                select(Employee).where(Employee.server_id == server_id)
            )
            return result.scalars().all()