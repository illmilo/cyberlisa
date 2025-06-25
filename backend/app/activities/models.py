from sqlalchemy.orm import relationship, Mapped, mapped_column
from backend.app.database import Base, str_uniq, int_pk, str_null_true
from sqlalchemy import select
from backend.app.database import async_session_maker
import asyncio

class Activity(Base):
    __tablename__ = "activitys"
    
    id: Mapped[int_pk]
    name: Mapped[str]
    url: Mapped[str]
    description: Mapped[str]
    os: Mapped[str]
    employees: Mapped[list["Employee"]] = relationship("Employee", secondary="employee_activity", back_populates="activities")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name!r}, url={self.url!r}, os={self.os!r}, employees={self.employees!r})"

    def __repr__(self):
        return str(self)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "description": self.description,
            "os": self.os,
            "employees": [
                {"id": employee.id, "name": employee.name, "surname": employee.surname}
                for employee in self.employees
            ] if self.employees else []
        }

    def get_actions_with_probabilities(self, employee_id=None):
        # Возвращает список dict: [{'id': ..., 'name': ..., 'probability': ...}, ...]
        # Если employee_id не указан, возвращает все активности без вероятности
        async def fetch():
            async with async_session_maker() as session:
                if employee_id is not None:
                    result = await session.execute(
                        select(Activity, employee_activity.c.probability)
                        .join(employee_activity, Activity.id == employee_activity.c.activity_id)
                        .where(employee_activity.c.employee_id == employee_id)
                    )
                    return [
                        {**activity.to_dict(), 'probability': probability}
                        for activity, probability in result.all()
                    ]
                else:
                    result = await session.execute(select(Activity))
                    return [activity.to_dict() for activity in result.scalars().all()]
        return asyncio.run(fetch()) 