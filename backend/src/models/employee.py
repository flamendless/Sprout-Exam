from pydantic import BaseModel, EmailStr, Field

from src.enums import EmployeeType
from src.models.base import DB, Filter, Pagination


class BenefitDB(DB):
    name: str
    description: str


class ProjectDB(DB):
    name: str
    description: str


class EmployeeDB(DB):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    type: EmployeeType
    number_of_leaves: int | None = Field(default=None)


class EmployeePatch(BaseModel):
    email: EmailStr | None = Field(default=None)
    password: str | None = Field(default=None)
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)
    type: EmployeeType | None = Field(default=None)
    number_of_leaves: int | None = Field(default=None)


class EmployeeResponse(EmployeeDB):
    password: str | None = Field(default=None, exclude=True)
    benefits: list[BenefitDB] | None = Field(default=None)
    projects: list[ProjectDB] | None = Field(default=None)


class EmployeePaginated(BaseModel):
    data: list[EmployeeResponse]
    pagination: Pagination


class EmployeeFilter(Filter):
    id: int | None = Field(default=None)
    email: EmailStr | None = Field(default=None)
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)
    type: EmployeeType | None = Field(default=None)
