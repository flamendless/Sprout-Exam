from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, status, Body
from fastapi.responses import Response

from src.const import EXC_RES_CREATE_FAILED, EXC_RES_NOT_FOUND
from src.context import pwd
from src.db import conn
from src.enums import AuditAction
from src.models.base import Pagination
from src.models.employee import (
    EmployeeCreate,
    EmployeeFilter,
    EmployeePaginated,
    EmployeePatch,
    EmployeeResponse,
)
from src.types import T_ADMIN
from src.utils import (
    create_audit,
    get_employee_benefits,
    get_employee_projects,
    get_filter_clause,
    get_update_clause,
    populate_employee,
    tuple_to_pydantic,
)

router = APIRouter(
    prefix="/employee",
    tags=["employee"],
)


@router.get(
    "/",
    response_model=EmployeePaginated,
)
async def get_employees(
    current_user: T_ADMIN,
    pagination: Annotated[Pagination, Depends()],
    filter_input: Annotated[EmployeeFilter, Depends()],
):
    sql: str = """
        SELECT
            id, created_at, updated_at,
            email, password, first_name,
            last_name, type, number_of_leaves,
            contract_end_date
        FROM
            tbl_employee
    """

    filter_data: dict = filter_input.get_data(filter_input)
    if filter_data:
        sql += get_filter_clause(filter_data)

    cur = conn.cursor()
    res_employees = cur.execute(sql, tuple(filter_data.values()))
    res_employees: list[tuple | None] = res_employees.fetchmany(
        pagination.per_page,
    )

    employee_ids: list[int] = [
        employee[0]
        for employee in res_employees
    ]
    projects: dict[list] = get_employee_projects(employee_ids)
    benefits: dict[list] = get_employee_benefits(employee_ids)

    data: list[EmployeeResponse] = [
        tuple_to_pydantic(EmployeeResponse, employee)
        for employee in res_employees
    ]

    d: EmployeeResponse
    for d in data:
        d = populate_employee(d, projects, benefits)

    return EmployeePaginated(data=data, pagination=pagination)


@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse,
)
async def get_employee_by_id(
    current_user: T_ADMIN,
    employee_id: int,
):
    sql: str = """
        SELECT
            id, created_at, updated_at,
            email, password, first_name,
            last_name, type, number_of_leaves
        FROM
            tbl_employee
        WHERE
            id = ?
    """

    cur = conn.cursor()
    res_employee = cur.execute(sql, (employee_id,))
    res_employee: tuple | None = res_employee.fetchone()
    if res_employee is None:
        raise EXC_RES_NOT_FOUND

    employee_ids: list[int] = [employee_id]
    projects: dict[list] = get_employee_projects(employee_ids)
    benefits: dict[list] = get_employee_benefits(employee_ids)
    res: EmployeeResponse = tuple_to_pydantic(EmployeeResponse, res_employee)
    res = populate_employee(res, projects, benefits)
    return res


@router.post(
    "/",
    response_model=EmployeeResponse,
)
async def create_employee(
    current_user: T_ADMIN,
    create_data: Annotated[EmployeeCreate, Body()],
    bg_tasks: BackgroundTasks,
):
    create_data.password = pwd.hash(create_data.password)
    data: dict = create_data.model_dump()

    sql: str = """
        INSERT INTO tbl_employee(
            email, password, first_name,
            last_name, type, number_of_leaves,
            contract_end_date, created_at, updated_at
        )
        VALUES(?, ?, ?, ?, ?, ?, ?, DATE('NOW'), DATE('NOW'))
    """
    cur = conn.cursor()
    res = cur.execute(sql, tuple(data.values()))
    conn.commit()
    if res.rowcount == 0:
        raise EXC_RES_CREATE_FAILED

    bg_tasks.add_task(
        create_audit,
        (
            res.lastrowid,
            "tbl_employee",
            AuditAction.CREATE.value,
            f"Created employee: {create_data.email}",
            datetime.now(tz=UTC)
        )
    )

    sql = """
        SELECT
            id, created_at, updated_at,
            email, password, first_name,
            last_name, type, number_of_leaves,
            contract_end_date
        FROM
            tbl_employee
        WHERE
            id = ?
    """
    res = cur.execute(sql, (res.lastrowid,))
    res = cur.fetchone()
    return tuple_to_pydantic(EmployeeResponse, res)


@router.patch(
    "/{employee_id}",
    response_class=Response,
)
async def patch_employee_by_id(
    current_user: T_ADMIN,
    employee_id: int,
    patch_data: Annotated[EmployeePatch, Body()],
    bg_tasks: BackgroundTasks,
):
    cur = conn.cursor()
    res_employee = cur.execute(
        "SELECT id FROM tbl_employee WHERE id = ?",
        (employee_id,),
    )
    res_employee: tuple | None = res_employee.fetchone()
    if res_employee is None:
        raise EXC_RES_NOT_FOUND

    if "password" in patch_data:
        patch_data["password"] = pwd.hash(patch_data["password"])

    patch_data_d: dict = patch_data.model_dump(exclude_none=True)
    if not patch_data_d:
        return Response(status_code=status.HTTP_200_OK)

    sql: str = "UPDATE tbl_employee"
    sql += get_update_clause(patch_data_d)
    sql += "WHERE id = ?;"

    cur = conn.cursor()
    res = cur.execute(sql, (*patch_data_d.values(), employee_id))
    conn.commit()
    if res.rowcount == 0:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    bg_tasks.add_task(
        create_audit,
        (
            employee_id,
            "tbl_employee",
            AuditAction.UPDATE.value,
            f"Updated employee: {employee_id}",
            datetime.now(tz=UTC)
        )
    )

    return Response(status_code=status.HTTP_200_OK)


@router.delete(
    "/{employee_id}",
    response_class=Response,
)
async def delete_employee_by_id(
    current_user: T_ADMIN,
    employee_id: int,
    bg_tasks: BackgroundTasks,
):
    if current_user.id == employee_id:
        return Response(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="Can't delete yourself",
        )

    cur = conn.cursor()
    res_employee = cur.execute(
        "SELECT id FROM tbl_employee WHERE id = ?",
        (employee_id,),
    )
    res_employee: tuple | None = res_employee.fetchone()
    if res_employee is None:
        raise EXC_RES_NOT_FOUND

    cur = conn.cursor()
    res = cur.execute("DELETE FROM tbl_employee WHERE id = ?", (employee_id,))
    conn.commit()
    if res.rowcount == 0:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    bg_tasks.add_task(
        create_audit,
        (
            employee_id,
            "tbl_employee",
            AuditAction.DELETE.value,
            f"Deleted employee: {employee_id}",
            datetime.now(tz=UTC)
        )
    )

    return Response(status_code=status.HTTP_200_OK)
