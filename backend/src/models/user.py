from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from src.enums import EmployeeType


class BenefitDB(BaseModel):
    id: int
    name: str
    description: str


class ProjectDB(BaseModel):
    id: int
    name: str
    description: str


class UserDB(BaseModel):
    id: int
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    type: EmployeeType
    number_of_leaves: int | None
    created_at: datetime
    updated_at: datetime


class UserResponse(UserDB):
    password: None = None
    benefits: list[BenefitDB] | None = Field(default=None)
    projects: list[ProjectDB] | None = Field(default=None)
