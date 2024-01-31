from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import Response
from pydantic import EmailStr

from src.const import EXC_RES_CREATE_FAILED, EXC_RES_NOT_FOUND
from src.context import pwd
from src.db import conn
from src.models.base import Pagination
from src.models.employee import (
    EmployeeCreate,
    EmployeeFilter,
    EmployeePaginated,
    EmployeePatch,
    EmployeeResponse,
)
from src.types import T_ADMIN
from src.utils import get_filter_clause, get_update_clause, tuple_to_pydantic

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
            last_name, type, number_of_leaves
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
    data: list[EmployeeResponse] = [
        tuple_to_pydantic(EmployeeResponse, employee)
        for employee in res_employees
    ]
    return EmployeePaginated(data=data, pagination=pagination)


@router.get(
    "/id={employee_id}",
    response_model=EmployeeResponse,
)
async def get_employee_by_id(
    current_user: T_ADMIN,
    employeed_id: int,
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
    res_employee = cur.execute(sql, (employeed_id,))
    res_employee: tuple | None = res_employee.fetchone()
    if res_employee is None:
        raise EXC_RES_NOT_FOUND
    return tuple_to_pydantic(EmployeeResponse, res_employee)


@router.get(
    "/email={email}",
    response_model=EmployeeResponse,
)
async def get_employee_by_email(
    current_user: T_ADMIN,
    email: EmailStr,
):
    sql: str = """
        SELECT
            id, created_at, updated_at,
            email, password, first_name,
            last_name, type, number_of_leaves
        FROM
            tbl_employee
        WHERE
            email = ?
    """

    cur = conn.cursor()
    res_employee = cur.execute(sql, (email,))
    res_employee: tuple | None = res_employee.fetchone()
    if res_employee is None:
        raise EXC_RES_NOT_FOUND
    return tuple_to_pydantic(EmployeeResponse, res_employee)


@router.post(
    "/",
    response_model=EmployeeResponse,
)
async def create_employee(
    current_user: T_ADMIN,
    create_data: Annotated[EmployeeCreate, Depends()],
):
    create_data.password = pwd.hash(create_data.password)
    data: dict = create_data.model_dump()

    sql: str = """
        INSERT INTO tbl_employee(
            email, password, first_name,
            last_name, type, number_of_leaves,
            created_at, updated_at
        )
        VALUES(?, ?, ?, ?, ?, ?, DATE('NOW'), DATE('NOW'))
    """
    cur = conn.cursor()
    res = cur.execute(sql, tuple(data.values()))
    conn.commit()
    if res.rowcount == 0:
        raise EXC_RES_CREATE_FAILED

    sql = """
        SELECT
            id, created_at, updated_at,
            email, password, first_name,
            last_name, type, number_of_leaves
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
    patch_data: Annotated[EmployeePatch, Depends()],
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

    patch_data: dict = patch_data.model_dump(exclude_none=True)
    if not patch_data:
        return Response(status_code=status.HTTP_200_OK)

    sql: str = "UPDATE tbl_employee"
    sql += get_update_clause(patch_data)
    sql += "WHERE id = ?;"

    cur = conn.cursor()
    res = cur.execute(sql, (*patch_data.values(), employee_id))
    conn.commit()
    if res.rowcount == 0:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(status_code=status.HTTP_200_OK)


@router.delete(
    "/{employee_id}",
    response_class=Response,
)
async def delete_employee_by_id(
    current_user: T_ADMIN,
    employee_id: int,
):
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
    return Response(status_code=status.HTTP_200_OK)
