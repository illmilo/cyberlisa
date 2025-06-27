from app.employees.schemas import EmployeeSchema


class RBEmp:
    def __init__(self, employee_id: int | None = None,
                 role: str | None = None,
                 os: str | None = None):
        self.id = employee_id
        self.role = role
        self.os = os

        
    def to_dict(self) -> dict:
        data = {'id': self.id, 'role': self.role, 'os': self.os}
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data