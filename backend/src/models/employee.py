from datetime import datetime
from typing import Any

from pydantic import BaseModel, EmailStr, Field, model_validator

from src.enums import EmployeeType
from src.models.base import DB, Filter, Pagination
from src.models.benefit import BenefitDB
from src.models.project import ProjectDB


class EmployeeDB(DB):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    type: EmployeeType
    number_of_leaves: int | None = Field(default=None)
    contract_end_date: datetime | None = Field(default=None)


class EmployeeCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    type: EmployeeType
    number_of_leaves: int | None = Field(default=None)
    contract_end_date: datetime | None = Field(default=None)

    @model_validator(mode="before")
    def validate_before(cls, data: dict) -> dict:
        if data["type"] in (
            EmployeeType.REGULAR.value,
            EmployeeType.ADMIN.value,
        ):
            del data["contract_end_date"]
        if data["type"] in (
            EmployeeType.CONTRACTUAL.value,
            EmployeeType.ADMIN.value,
        ):
            del data["number_of_leaves"]
        return data

    @model_validator(mode="after")
    @classmethod
    def validate_after(cls, data: Any) -> Any:
        if (
            (data.type == EmployeeType.CONTRACTUAL) and
            (not data.contract_end_date)
        ):
            raise ValueError(
                "REQUIRED: contract end date for contractual employee"
            )
        return data


class EmployeePatch(BaseModel):
    email: EmailStr | None = Field(default=None)
    password: str | None = Field(default=None)
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)
    type: EmployeeType | None = Field(default=None)
    number_of_leaves: int | None = Field(default=None)
    contract_end_date: datetime | None = Field(default=None)


class EmployeeResponse(EmployeeDB):
    password: str | None = Field(default=None, exclude=True)
    benefits: list[BenefitDB] | None = Field(default=None)
    projects: list[ProjectDB] | None = Field(default=None)

    @model_validator(mode="after")
    @classmethod
    def validate(cls, data: Any) -> Any:
        if data.type == EmployeeType.REGULAR:
            data.contract_end_date = None
        elif data.type == EmployeeType.CONTRACTUAL:
            data.number_of_leaves = None
        return data


class EmployeePaginated(BaseModel):
    data: list[EmployeeResponse]
    pagination: Pagination


class EmployeeFilter(Filter):
    id: int | None = Field(default=None)
    email: EmailStr | None = Field(default=None)
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)
    type: EmployeeType | None = Field(default=None)
