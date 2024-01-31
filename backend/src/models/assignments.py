from pydantic import BaseModel


class ProjectAssignEmployees(BaseModel):
    employee_ids: list[int]


class BenefitAssignEmployees(BaseModel):
    employee_ids: list[int]
