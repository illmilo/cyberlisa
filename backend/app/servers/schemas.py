from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from app.employees.schemas import EmployeeSchema


class ServerSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str = Field(..., min_length=1, max_length=50, description="Название сервера, от 1 до 50 символов")
    ip: str = Field(..., min_length=1, max_length=15, description="IP сервера, от 1 до 15 символов")
    port: str = Field(..., min_length=1, max_length=5, description="Порт сервера, от 1 до 5 символов")

class ServerCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Название сервера, от 1 до 50 символов")
    ip: str = Field(..., min_length=1, max_length=15, description="IP сервера, от 1 до 15 символов")
    port: str = Field(..., min_length=1, max_length=5, description="Порт сервера, от 1 до 5 символов")

class ServerUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50, description="Название сервера, от 1 до 50 символов")
    ip: Optional[str] = Field(None, min_length=1, max_length=15, description="IP сервера, от 1 до 15 символов")
    port: Optional[str] = Field(None, min_length=1, max_length=5, description="Порт сервера, от 1 до 5 символов")
