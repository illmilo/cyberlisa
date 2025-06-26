from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base, str_uniq, int_pk, str_null_true

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