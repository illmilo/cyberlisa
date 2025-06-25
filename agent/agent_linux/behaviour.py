import time
import json
from croniter import croniter
import datetime
import random
import asyncio
from agent.agent_linux.handlers import DevHandler, AdminHandler#, UserHandler
from backend.app.database import async_session_maker
from backend.app.employees.models import Employee

#надо сделать чтобы конфиг json брался из бд и сюда передавался

class Behaviour:
    def __init__ (self, config):
        self.config = config
        self.activity_rate = self.config.get("activity_rate", 1.0)
        self.handler = self.get_handler()
    
    def isActive(self):
        now = datetime.datetime.now().time()
        start = datetime.time.fromisoformat(self.config["work_start_time"])
        end = datetime.time.fromisoformat(self.config["work_end_time"])
        return start <= now < end
    
    async def get_next_action(self):
        if asyncio.iscoroutinefunction(self.handler.work):
            return await self.handler.work()
        else:
            return self.handler.work()
    
    def get_handler(self):
        if self.config["role"] == "dev":
            return DevHandler()
        elif self.config["role"] == "admin":
            return AdminHandler()
        elif self.config["role"] == "user":
            return UserHandler()
        else:
            raise ValueError(f"Unknown role: {self.config['role']}")

    async def set_online(self, online: bool = True):
        async with async_session_maker() as session:
            employee = await session.get(Employee, self.config["employee_id"])
        if employee:
            employee.online = online
            await session.commit()

    async def set_activity_now(self, activity_id: int):
        async with async_session_maker() as session:
            employee = await session.get(Employee, self.config["employee_id"])
        if employee:
            employee.activity_now = activity_id
            await session.commit()

    
    async def run_loop(self, action_func=None):
        while True:
            if self.isActive():
                await self.set_online(True)
                if random.random() < min(self.activity_rate, 1.0):
                    action = await self.get_next_action()
                    print(f"Выполняется действие: {action['name']}")
                    await self.set_activity_now(action["name"])
                    action_duration = random.uniform(1, 3) / max(self.activity_rate, 0.1)
                    action["run"]()  # Выполнение действия
                    await asyncio.sleep(action_duration)
                pause = random.uniform(1, 5) / max(self.activity_rate, 0.1)
                await asyncio.sleep(pause)
            else:
                await self.set_online(False)      
                await asyncio.sleep(60)
    