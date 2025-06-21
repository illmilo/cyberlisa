from sqlalchemy import ForeignKey, text, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base, str_uniq, int_pk, str_null_true
from app.activities.models import Activity

class Employee(Base):
    id: Mapped[int_pk]
    name: Mapped[str]
    surname: Mapped[str]
    role: Mapped[str]
    online: Mapped[bool]
    os: Mapped[str]
    activity_now: Mapped[int] = mapped_column(ForeignKey("activitys.id"), nullable=True)
    activities: Mapped[list["Activity"]] = relationship("Activity", back_populates="employees")

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"name={self.name!r},"
                f"surname={self.surname!r},"
                f"role={self.role!r},"
                f"online={self.online!r},"
                f"os={self.os!r},"
                f"activity_now={self.activity_now!r},"
                f"activities={self.activities!r})")

    def __repr__(self):
        return str(self)
    def to_dict(self): 
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "role": self.role,
            "online": self.online,
            "os": self.os,
            "activity_now": self.activity_now,
            "activities": [activity.to_dict() for activity in (self.activities or list())]
        }

