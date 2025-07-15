from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from app.employees.schemas import EmployeeSchema


class ServerSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str = Field(..., min_length=1, max_length=50, description="Название сервера, от 1 до 50 символов")
    password: str = Field(..., min_length=1, max_length=15, description="Пароль пользователя, от 1 до 15 символов")
    server_key: str = Field(..., min_length=1, max_length=50, description="Ключ сервера, от 1 до 50 символов")
    

class ServerCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Название сервера, от 1 до 50 символов")
    password: str = Field(..., min_length=1, max_length=15, description="Пароль пользователя, от 1 до 15 символов")
    server_key: str = Field(..., min_length=1, max_length=50, description="Ключ сервера, от 1 до 50 символов")

class ServerUpdateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Название сервера, от 1 до 50 символов")
    password: str = Field(..., min_length=1, max_length=15, description="Пароль пользователя, от 1 до 15 символов")
    server_key: str = Field(..., min_length=1, max_length=50, description="Ключ сервера, от 1 до 50 символов")
