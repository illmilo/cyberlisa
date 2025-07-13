from sqlalchemy import ForeignKey, text, Text, Table, Column, Time, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base, str_uniq, int_pk, str_null_true
from app.activities.models import Activity
from app.servers.models import Server

employee_activity = Table(
    'employee_activity',
    Base.metadata,
    Column('employee_id', ForeignKey('employees.id'), primary_key=True),
    Column('activity_id', ForeignKey('activitys.id'), primary_key=True)
)

class Employee(Base):
    id: Mapped[int_pk]
    name: Mapped[str]
    role: Mapped[str]
    online: Mapped[bool]
    os: Mapped[str]
    activity_now: Mapped[int] = mapped_column(ForeignKey("activitys.id"), nullable=True)
    activities: Mapped[list["Activity"]] = relationship("Activity", secondary=employee_activity, back_populates="employees")
    work_start_time = mapped_column(Time, nullable=True)
    work_end_time = mapped_column(Time, nullable=True)
    activity_rate = mapped_column(Float, nullable=True)
    server_id: Mapped[int] = mapped_column(ForeignKey('servers.id'), default = 1)
    server: Mapped["Server"] = relationship("Server", back_populates="employees")

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"name={self.name!r},"
                f"role={self.role!r},"
                f"online={self.online!r},"
                f"os={self.os!r},"
                f"activity_now={self.activity_now!r},"
                f"activities={self.activities!r},"
                f"server_id={self.server_id!r})")

    def __repr__(self):
        return str(self)
    
    def to_dict(self): 
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "online": self.online,
            "os": self.os,
            "activity_now": self.activity_now,
            "activities": [activity.to_dict() for activity in (self.activities or list())],
            "work_start_time": self.work_start_time.isoformat() if self.work_start_time else None,
            "work_end_time": self.work_end_time.isoformat() if self.work_end_time else None,
            "activity_rate": self.activity_rate,
            "server_id": self.server_id
        }

# Важно: после удаления поля surname требуется миграция Alembic для удаления столбца из БД

