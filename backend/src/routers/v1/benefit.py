from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, status
from fastapi.responses import Response

from src.const import EXC_RES_CREATE_FAILED, EXC_RES_NOT_FOUND
from src.db import conn
from src.enums import AuditAction
from src.models.base import Pagination
from src.models.benefit import (
    BenefitCreate,
    BenefitFilter,
    BenefitPaginated,
    BenefitPatch,
    BenefitResponse,
)
from src.types import T_ADMIN
from src.utils import (
    create_audit,
    get_filter_clause,
    get_update_clause,
    tuple_to_pydantic,
)

router = APIRouter(
    prefix="/benefit",
    tags=["benefit"],
)


@router.get(
    "/",
    response_model=BenefitPaginated,
)
async def get_benefits(
    current_user: T_ADMIN,
    pagination: Annotated[Pagination, Depends()],
    filter_input: Annotated[BenefitFilter, Depends()],
):
    sql: str = """
        SELECT
            id, created_at, updated_at,
            name, description
        FROM
            tbl_benefit
    """

    filter_data: dict = filter_input.get_data(filter_input)
    if filter_data:
        sql += get_filter_clause(filter_data)

    cur = conn.cursor()
    res_benefits = cur.execute(sql, tuple(filter_data.values()))
    res_benefits: list[tuple | None] = res_benefits.fetchmany(
        pagination.per_page,
    )
    data: list[BenefitResponse] = [
        tuple_to_pydantic(BenefitResponse, benefit)
        for benefit in res_benefits
    ]
    return BenefitPaginated(data=data, pagination=pagination)


@router.get(
    "/id={benefit_id}",
    response_model=BenefitResponse,
)
async def get_benefit_by_id(
    current_user: T_ADMIN,
    benefit_id: int,
):
    sql: str = """
        SELECT
            id, created_at, updated_at,
            name, description
        FROM
            tbl_benefit
        WHERE
            id = ?
    """

    cur = conn.cursor()
    res_benefit = cur.execute(sql, (benefit_id,))
    res_benefit: tuple | None = res_benefit.fetchone()
    if res_benefit is None:
        raise EXC_RES_NOT_FOUND
    return tuple_to_pydantic(BenefitResponse, res_benefit)


@router.post(
    "/",
    response_model=BenefitResponse,
)
async def create_benefit(
    current_user: T_ADMIN,
    create_data: Annotated[BenefitCreate, Depends()],
    bg_tasks: BackgroundTasks,
):
    data: dict = create_data.model_dump()

    sql: str = """
        INSERT INTO tbl_benefit(
            name, description,
            created_at, updated_at
        )
        VALUES(?, ?, DATE('NOW'), DATE('NOW'))
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
            "tbl_benefit",
            AuditAction.CREATE.value,
            f"Created benefit: {create_data.name}",
            datetime.now(tz=UTC)
        )
    )

    sql = """
        SELECT
            id, created_at, updated_at,
            name, description
        FROM
            tbl_benefit
        WHERE
            id = ?
    """
    res = cur.execute(sql, (res.lastrowid,))
    res = cur.fetchone()
    return tuple_to_pydantic(BenefitResponse, res)


@router.patch(
    "/{benefit_id}",
    response_class=Response,
)
async def patch_benefit_by_id(
    current_user: T_ADMIN,
    benefit_id: int,
    patch_data: Annotated[BenefitPatch, Depends()],
    bg_tasks: BackgroundTasks,
):
    cur = conn.cursor()
    res_benefit = cur.execute(
        "SELECT id FROM tbl_benefit WHERE id = ?",
        (benefit_id,),
    )
    res_benefit: tuple | None = res_benefit.fetchone()
    if res_benefit is None:
        raise EXC_RES_NOT_FOUND

    patch_data_d: dict = patch_data.model_dump(exclude_none=True)
    if not patch_data_d:
        return Response(status_code=status.HTTP_200_OK)

    sql: str = "UPDATE tbl_benefit"
    sql += get_update_clause(patch_data_d)
    sql += "WHERE id = ?;"

    cur = conn.cursor()
    res = cur.execute(sql, (*patch_data_d.values(), benefit_id))
    conn.commit()
    if res.rowcount == 0:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    bg_tasks.add_task(
        create_audit,
        (
            res.lastrowid,
            "tbl_benefit",
            AuditAction.UPDATE.value,
            f"Updated benefit: {benefit_id}",
            datetime.now(tz=UTC)
        )
    )

    return Response(status_code=status.HTTP_200_OK)


@router.delete(
    "/{benefit_id}",
    response_class=Response,
)
async def delete_benefit_by_id(
    current_user: T_ADMIN,
    benefit_id: int,
    bg_tasks: BackgroundTasks,
):
    cur = conn.cursor()
    res_benefit = cur.execute(
        "SELECT id FROM tbl_benefit WHERE id = ?",
        (benefit_id,),
    )
    res_benefit: tuple | None = res_benefit.fetchone()
    if res_benefit is None:
        raise EXC_RES_NOT_FOUND

    cur = conn.cursor()
    res = cur.execute("DELETE FROM tbl_benefit WHERE id = ?", (benefit_id,))
    conn.commit()
    if res.rowcount == 0:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    bg_tasks.add_task(
        create_audit,
        (
            res.lastrowid,
            "tbl_benefit",
            AuditAction.DELETE.value,
            f"Deleted benefit: {benefit_id}",
            datetime.now(tz=UTC)
        )
    )

    return Response(status_code=status.HTTP_200_OK)
