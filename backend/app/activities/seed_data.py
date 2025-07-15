# from app.activities.models import Activity
# from app.database import async_session_maker

# async def seed_activities():
#     async with async_session_maker() as session:
#         existing_activities = await session.query(Activity).all()
#         if existing_activities:
#             print("Активности уже существуют, пропускаем заполнение")
#             return

#         # Создаем активности
#         activities = [
#             Activity(
#                 name="Firefox",
#                 url="duckduckgo.com",
#                 description="Веб-браузер для поиска и просмотра веб-страниц",
#                 os="linux"
#             ),
#             Activity(
#                 name="LibreOffice Calc",
#                 url=None,
#                 description="Электронные таблицы для работы с данными и расчетами",
#                 os="linux"
#             ),
#             Activity(
#                 name="LibreOffice Writer", 
#                 url=None,
#                 description="Текстовый редактор для создания документов",
#                 os="linux"
#             )
#         ]
        
#         session.add_all(activities)
#         await session.commit()
#         print("Активности успешно добавлены в базу данных")

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(seed_activities()) 