from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum

class OS(Enum):
    WINDOWS = "windows"
    LINUX = "linux"
    UNKNOWN = "unknown"


class EmployeeShallowSchema(BaseModel):
    id: int
    name: str


class ActivitySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str = Field(..., min_length=1, max_length=50, description="Название активности, от 1 до 50 символов")
    url: Optional[str] = Field(None, min_length=1, max_length=200, description="URL активности, от 1 до 200 символов")
    description: str = Field(..., description="Описание активности")
    os: OS = Field(..., description="Операционная система")
    employees: List[EmployeeShallowSchema] = Field(default_factory=list, description="Агенты, которым назначена активность")


class ActivityCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Название активности, от 1 до 50 символов")
    url: Optional[str] = Field(None, min_length=1, max_length=200, description="URL активности, от 1 до 200 символов")
    description: str = Field(..., description="Описание активности")
    os: OS = Field(..., description="Операционная система")


class ActivityUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50, description="Название активности, от 1 до 50 символов")
    url: Optional[str] = Field(None, min_length=1, max_length=200, description="URL активности, от 1 до 200 символов")
    description: Optional[str] = Field(None, description="Описание активности")
    os: Optional[OS] = Field(None, description="Операционная система")


class ActivityShallowSchema(BaseModel):
    id: int
    name: str
    url: Optional[str] = None
    description: str
    os: OS