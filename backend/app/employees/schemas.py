from datetime import datetime, date, time
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
    name: str = Field(..., min_length=1, max_length=50, description="Имя агента, от 1 до 50 символов")
    role: Role = Field(..., description="Роль агента")
    os: OS = Field(..., description="Операционная система агента")
    online: bool = Field(..., description="Статус онлайн")
    activity_now: Optional[str] = Field(None, description="Активность")
    activities: Optional[List["ActivitySchema"]] = Field(default_factory=list, description="Активности")
    work_start_time: Optional[time] = Field(None, description="Время начала работы")
    work_end_time: Optional[time] = Field(None, description="Время окончания работы")
    activity_rate: Optional[float] = Field(None, description="Коэффициент активности")
    server_id: Optional[int] = Field(None, description="ID сервера")


class EmployeeSchemaWnoActivities(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str = Field(..., min_length=1, max_length=50, description="Имя агента, от 1 до 50 символов")
    role: Role = Field(..., description="Роль агента")
    os: OS = Field(..., description="Операционная система агента")
    online: bool = Field(..., description="Статус онлайн")
    activity_now: Optional[str] = Field(None, description="Активность")
    work_start_time: Optional[time] = Field(None, description="Время начала работы")
    work_end_time: Optional[time] = Field(None, description="Время окончания работы")
    activity_rate: Optional[float] = Field(None, description="Коэффициент активности")
    server_id: Optional[int] = Field(None, description="ID сервера")

class EmployeeCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Имя агента, от 1 до 50 символов")
    role: Role = Field(..., description="Роль агента")
    os: OS = Field(..., description="Операционная система агента")
    online: bool = Field(..., description="Статус онлайн")
    activity_now: Optional[int] = Field(None, description="ID активности")
    work_start_time: Optional[time] = Field(None, description="Время начала работы")
    work_end_time: Optional[time] = Field(None, description="Время окончания работы")
    activity_rate: Optional[float] = Field(None, description="Коэффициент активности")
    server_id: Optional[int] = Field(None, description="ID сервера")

class EmployeeUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50, description="Имя агента, от 1 до 50 символов")
    role: Optional[Role] = Field(None, description="Роль агента")
    os: Optional[OS] = Field(None, description="Операционная система агента")
    online: Optional[bool] = Field(None, description="Статус онлайн")
    activity_now: Optional[int] = Field(None, description="ID активности")
    work_start_time: Optional[time] = Field(None, description="Время начала работы")
    work_end_time: Optional[time] = Field(None, description="Время окончания работы")
    activity_rate: Optional[float] = Field(None, description="Коэффициент активности")
    server_id: Optional[int] = Field(None, description="ID сервера")
from app.activities.schemas import ActivitySchema
EmployeeSchema.model_rebuild()
