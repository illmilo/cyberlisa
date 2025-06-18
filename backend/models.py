from pydantic import BaseModel, Field, field_validator, ValidationError
from datetime import datetime, date
from enum import Enum

class RoleEnum(str, Enum):
    admin = "admin"
    user = "user"
    dev = "dev"

class EmployeeModel(BaseModel):
    id: int = Field(default=..., description="The id of the employee")
    name: str = Field(default=..., min_length=1, max_length=50, description="The name of the employee")
    surname: str = Field(default=..., min_length=1, max_length=50, description="The surname of the employee")
    role: RoleEnum = Field(default="user", description="The role of the employee")
    # timebegin: datetime = Field(default=..., description="The time the employee starts working")
    # timeend: datetime = Field(default=..., description="The time the employee finishes working")
    # last_activity: datetime = Field(default=datetime.now(), description="The time the employee last activity")
    # last_seen: datetime = Field(default=datetime.now(), description="The time the employee last seen")
    # current_program: str = Field(default="", description="The current program the employee is using")
    # current_url: str = Field(default="", description="The current url the employee is on")

class Program(BaseModel):
    id: int
    name: str

class Website(BaseModel):
    id: int
    name: str
    url: str