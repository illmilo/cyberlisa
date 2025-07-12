#!/usr/bin/env python3
"""
Скрипт для заполнения базы данных активностями
"""
import asyncio
import sys
import os

# Добавляем путь к модулям приложения
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.activities.models import Activity
from app.database import async_session_maker

async def seed_activities():
    """Заполнить базу данных начальными активностями"""
    async with async_session_maker() as session:
        # Проверяем, есть ли уже активности
        from sqlalchemy import select
        result = await session.execute(select(Activity))
        existing_activities = result.scalars().all()
        
        if existing_activities:
            print("Активности уже существуют, пропускаем заполнение")
            return

        # Создаем активности
        activities = [
            Activity(
                name="Firefox",
                url="https://duckduckgo.com",  # Добавляем протокол https://
                description="Веб-браузер для поиска и просмотра веб-страниц",
                os="linux"
            ),
            Activity(
                name="LibreOffice Calc",
                url=None,
                description="Электронные таблицы для работы с данными и расчетами",
                os="linux"
            ),
            Activity(
                name="LibreOffice Writer", 
                url=None,
                description="Текстовый редактор для создания документов",
                os="linux"
            )
        ]
        
        session.add_all(activities)
        await session.commit()
        print("Активности успешно добавлены в базу данных:")
        for activity in activities:
            print(f"  - {activity.name}: {activity.description}")

if __name__ == "__main__":
    asyncio.run(seed_activities()) 