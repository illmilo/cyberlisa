from sqlalchemy import ForeignKey, text, Text, Table, Column, Time, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base, str_uniq, int_pk, str_null_true

# server_employee = Table(
#     'server_employee',
#     Base.metadata,
#     Column('server_id', ForeignKey('servers.id'), primary_key=True),
#     Column('employee_id', ForeignKey('employees.id'), primary_key=True)
# )



class Server(Base):
    id: Mapped[int_pk]
    name: Mapped[str]
    password: Mapped[str]
    server_key: Mapped[str]
    employees: Mapped[list["Employee"]] = relationship("Employee", back_populates="server")

def __str__(self):
    return (f"{self.__class__.__name__}(id={self.id}, "
            f"name={self.name!r},"
            f"password={self.password!r},"
            f"server_key={self.server_key!r},"
            f"employees={self.employees!r})")


def __repr__(self):
    return str(self)

def to_dict(self):
    return {
        "id": self.id,
        "name": self.name,
        "password": self.password,
        "server_key": self.server_key,
        "employees": [
            {"id": employee.id, "name": employee.name, "surname": employee.surname}
            for employee in self.employees
        ] if self.employees else []
    }

