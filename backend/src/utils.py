from collections import defaultdict
from enum import Enum
from functools import cache
from typing import Any

from pydantic import BaseModel

from src.db import new_conn
from src.enums import EmployeeType
from src.models.benefit import BenefitResponse
from src.models.employee import EmployeeResponse
from src.models.project import ProjectResponse


def tuple_to_pydantic(pydantic_class: BaseModel, data: tuple) -> BaseModel:
    return pydantic_class(
        **{
            k: v
            for k, v in zip(pydantic_class.model_fields.keys(), data)
        }
    )


@cache
def is_value_in_enum(enum_class: Enum, value: Any) -> bool:
    for e in enum_class:
        if e.value == value:
            return True
    return False


def get_filter_clause(filter_data: dict) -> str:
    sql = "WHERE\n"
    wheres: list[str] = [
        f"{k} = ?"
        for k in filter_data.keys()
    ]
    sql += " AND ".join(wheres)
    sql += "\n"
    return sql


def get_update_clause(update_data: dict) -> str:
    sql = "\nSET\n"
    updates: list[str] = [
        f"{k} = ?"
        for k in update_data.keys()
    ]
    sql += ", ".join(updates)
    sql += "\n"
    return sql


def create_audit(data: tuple) -> None:
    conn = new_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO tbl_audit(
            auditor_id,
            table_name,
            action,
            message,
            created_at
        )
        VALUES(?, ?, ?, ?, ?)
    """, data)
    conn.commit()


def get_employee_projects(employee_ids: list[int]) -> dict[list]:
    qms: str = ("?, " * (len(employee_ids) - 1)) + "?"
    sql_projects: str = """
        SELECT
            tbl_employee_project.employee_id,
            tbl_project.id,
            tbl_project.created_at, tbl_project.updated_at,
            tbl_project.name, tbl_project.description
        FROM tbl_project
        INNER JOIN
            tbl_employee_project ON
            tbl_employee_project.project_id = tbl_project.id
        WHERE
            tbl_employee_project.employee_id IN (%s)
    """ % qms
    cur = new_conn().cursor()
    res_projects = cur.execute(sql_projects, tuple(employee_ids))
    res_projects = res_projects.fetchall()
    projects = defaultdict(list)
    for project in res_projects:
        rem = list(project)
        rem.pop(0)
        projects[project[0]].append(tuple(rem))

    return projects


def get_employee_benefits(employee_ids: list[int]) -> dict[list]:
    qms: str = ("?, " * (len(employee_ids) - 1)) + "?"
    sql_benefits: str = """
        SELECT
            tbl_employee_benefit.employee_id,
            tbl_benefit.id,
            tbl_benefit.created_at, tbl_benefit.updated_at,
            tbl_benefit.name, tbl_benefit.description
        FROM tbl_benefit
        INNER JOIN
            tbl_employee_benefit ON
            tbl_employee_benefit.benefit_id = tbl_benefit.id
        WHERE
            tbl_employee_benefit.employee_id IN (%s)
    """ % qms
    cur = new_conn().cursor()
    res_benefits = cur.execute(sql_benefits, tuple(employee_ids))
    res_benefits = res_benefits.fetchall()
    benefits = defaultdict(list)
    for benefit in res_benefits:
        rem = list(benefit)
        rem.pop(0)
        benefits[benefit[0]].append(tuple(rem))

    return benefits


def populate_employee(
    employee: EmployeeResponse,
    projects: dict[list],
    benefits: dict[list]
) -> None:
    if employee.type in (EmployeeType.REGULAR, EmployeeType.ADMIN):
        employee.benefits = [
            tuple_to_pydantic(BenefitResponse, benefit)
            for benefit in benefits[employee.id]
        ]
    if employee.type in (EmployeeType.CONTRACTUAL, EmployeeType.ADMIN):
        employee.projects = [
            tuple_to_pydantic(ProjectResponse, project)
            for project in projects[employee.id]
        ]
    return employee
