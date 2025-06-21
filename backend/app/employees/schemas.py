from datetime import datetime, date
from typing import Optional, List
import re
from pydantic import BaseModel, Field, EmailStr, ConfigDict

from enum import Enum


class Role(Enum):
    ADMIN = "admin"
    USER = "user"
    DEV = "dev"


class OS(Enum):
    WINDOWS = "windows"
    LINUX = "linux"


class EmployeeSchema(BaseModel):   
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str = Field(..., min_length=1, max_length=50, description="Имя сотрудника, от 1 до 50 символов")
    surname: str = Field(..., min_length=1, max_length=50, description="Фамилия сотрудника, от 1 до 50 символов")
    role: Role = Field(..., description="Роль сотрудника")
    os: OS = Field(..., description="Операционная система")
    online: bool = Field(..., description="Статус онлайн")
    activity_now: Optional[str] = Field(None, description="Активность")
    activities: Optional[List["ActivitySchema"]] = Field(default_factory=list, description="Активности")
    

class EmployeeCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Имя сотрудника, от 1 до 50 символов")
    surname: str = Field(..., min_length=1, max_length=50, description="Фамилия сотрудника, от 1 до 50 символов")
    role: Role = Field(..., description="Роль сотрудника")
    os: OS = Field(..., description="Операционная система")
    online: bool = Field(..., description="Статус онлайн")
    activity_now: Optional[int] = Field(None, description="ID активности")

class EmployeeUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50, description="Имя сотрудника, от 1 до 50 символов")
    surname: Optional[str] = Field(None, min_length=1, max_length=50, description="Фамилия сотрудника, от 1 до 50 символов")
    role: Optional[Role] = Field(None, description="Роль сотрудника")
    os: Optional[OS] = Field(None, description="Операционная система")
    online: Optional[bool] = Field(None, description="Статус онлайн")
    activity_now: Optional[int] = Field(None, description="ID активности")

# Импорт в конце файла для избежания циклических ссылок
from app.activities.schemas import ActivitySchema
EmployeeSchema.model_rebuild()
