from datetime import datetime, date, time
from typing import Optional, List
import re
from pydantic import BaseModel, Field, ConfigDict
from app.roles.schemas import RoleNameSchema

from enum import Enum

class OS(Enum):
    WINDOWS = "windows"
    LINUX = "linux"


class ActivityShallowSchema(BaseModel):
    id: int
    name: str
    url: Optional[str] = None
    description: Optional[str] = None
    os: Optional[OS] = None


class EmployeeSchema(BaseModel):   
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str = Field(..., min_length=1, max_length=50, description="Имя агента, от 1 до 50 символов")
    role: Optional[RoleNameSchema] = Field(None, description="Роль агента")
    os: OS = Field(..., description="Операционная система агента")
    activities: Optional[List[ActivityShallowSchema]] = Field(default_factory=list, description="Активности")
    work_start_time: Optional[time] = Field(None, description="Время начала работы")
    work_end_time: Optional[time] = Field(None, description="Время окончания работы")
    activity_rate: Optional[float] = Field(None, description="Коэффициент активности")
    server_id: Optional[int] = Field(None, description="ID сервера")
    last_heartbeat: Optional[datetime] = Field(None, description="Время последнего heartbeat")
    agent_status: Optional[str] = None
    heartbeat_status: Optional[str] = None


class EmployeeSchemaWnoActivities(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str = Field(..., min_length=1, max_length=50, description="Имя агента, от 1 до 50 символов")
    role: Optional[RoleNameSchema] = Field(None, description="Роль агента")
    os: OS = Field(..., description="Операционная система агента")
    work_start_time: Optional[time] = Field(None, description="Время начала работы")
    work_end_time: Optional[time] = Field(None, description="Время окончания работы")
    activity_rate: Optional[float] = Field(None, description="Коэффициент активности")
    server_id: Optional[int] = Field(None, description="ID сервера")
    last_heartbeat: Optional[datetime] = Field(None, description="Время последнего heartbeat")
    agent_status: Optional[str] = None
    heartbeat_status: Optional[str] = None

class EmployeeCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Имя агента, от 1 до 50 символов")
    role_id: Optional[int] = Field(None, description="ID роли агента")
    os: OS = Field(..., description="Операционная система агента")
    work_start_time: Optional[time] = Field(None, description="Время начала работы")
    work_end_time: Optional[time] = Field(None, description="Время окончания работы")
    activity_rate: Optional[float] = Field(None, description="Коэффициент активности")
    server_id: Optional[int] = Field(None, description="ID сервера")
    last_heartbeat: Optional[datetime] = Field(None, description="Время последнего heartbeat")
    agent_status: Optional[str] = None

class EmployeeUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50, description="Имя агента, от 1 до 50 символов")
    role_id: Optional[int] = Field(None, description="ID роли агента")
    os: Optional[OS] = Field(None, description="Операционная система агента")
    work_start_time: Optional[time] = Field(None, description="Время начала работы")
    work_end_time: Optional[time] = Field(None, description="Время окончания работы")
    activity_rate: Optional[float] = Field(None, description="Коэффициент активности")
    server_id: Optional[int] = Field(None, description="ID сервера")
    last_heartbeat: Optional[datetime] = Field(None, description="Время последнего heartbeat")
    agent_status: Optional[str] = None
from app.activities.schemas import ActivitySchema
EmployeeSchema.model_rebuild()
