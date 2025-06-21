import asyncio
from app.database import async_session_maker
import sqlalchemy as sa

async def check_tables():
    async with async_session_maker() as session:
        # Получаем список таблиц
        result = await session.execute(sa.text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name"))
        tables = [row[0] for row in result]
        print("Tables in database:")
        for table in tables:
            print(f"  - {table}")
        
        # Проверяем структуру таблицы employees
        print("\nColumns in employees table:")
        result = await session.execute(sa.text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'employees' ORDER BY ordinal_position"))
        for row in result:
            print(f"  - {row[0]}: {row[1]}")
        
        # Проверяем структуру таблицы activitys
        print("\nColumns in activitys table:")
        result = await session.execute(sa.text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'activitys' ORDER BY ordinal_position"))
        for row in result:
            print(f"  - {row[0]}: {row[1]}")

if __name__ == "__main__":
    asyncio.run(check_tables()) 