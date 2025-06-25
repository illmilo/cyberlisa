import sys
import asyncio
import json
sys.path.append('../../backend/app')
from backend.app.employees.dao import EmployeeDAO
import agent.agent_linux.behaviour as behaviour
import asyncpg
from backend.app.employees.models import Employee
from backend.app.activities.models import Activity
from backend.app.database import async_session_maker
from backend.app.dao.base import BaseDAO

running_agents = {}

async def agent_worker(employee_id):
    config = await EmployeeDAO.get_agent_config_from_db(employee_id)
    if not config:
        print(f"Employee {employee_id} not found!")
        return
    agent = behaviour.Behaviour(config)
    async def action_func(action):
        print(f"Employee {employee_id} выполняет действие: {action['name']}")
    await agent.run_loop(action_func)

def on_notify(connection, pid, channel, payload):
    asyncio.create_task(handle_notify(payload))

async def handle_notify(payload):
    data = json.loads(payload)
    op = data.get('operation')
    emp_id = data.get('id')
    os_val = data.get('os', None)
    if op == 'DELETE':
        if emp_id in running_agents:
            print(f"Остановка агента для удалённого сотрудника {emp_id}")
            running_agents[emp_id].cancel()
            del running_agents[emp_id]
    elif op in ('INSERT', 'UPDATE'):
        if os_val != 'linux':
            # Если сотрудник сменил ОС — останавливаем агента
            if emp_id in running_agents:
                print(f"Остановка агента (смена ОС) {emp_id}")
                running_agents[emp_id].cancel()
                del running_agents[emp_id]
            return
        # Если сотрудник новый или изменился — перезапускаем агента
        if emp_id in running_agents:
            print(f"Перезапуск агента для сотрудника {emp_id}")
            running_agents[emp_id].cancel()
        print(f"Запуск агента для сотрудника {emp_id}")
        task = asyncio.create_task(agent_worker(emp_id))
        running_agents[emp_id] = task

async def listen_notifications():
    conn = await asyncpg.connect(dsn="postgresql://lisoon:12345@localhost:5433/fast_api")
    await conn.add_listener('employees_channel', on_notify)
    print("Слушаю события employees_channel...")
    while True:
        await asyncio.sleep(3600)  # держим соединение открытым``

async def main():
    # При старте — запустить агентов для всех linux-сотрудников
    from backend.app.database import async_session_maker
    async with async_session_maker() as session:
        employees = await session.execute(
            Employee.__table__.select().where(Employee.os == "linux")
        )
        employee_ids = employees.scalars().all()
    for emp_id in employee_ids:
        if emp_id not in running_agents:
            print(f"Запуск агента для сотрудника {emp_id}")
            task = asyncio.create_task(agent_worker(emp_id))
            running_agents[emp_id] = task
    # Запускаем слушатель событий
    await listen_notifications()

if __name__ == "__main__":
    asyncio.run(main())
