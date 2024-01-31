from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, status
from fastapi.responses import Response

from src.const import EXC_RES_CREATE_FAILED, EXC_RES_NOT_FOUND
from src.db import conn
from src.enums import AuditAction
from src.models.base import Pagination
from src.models.project import (
    ProjectCreate,
    ProjectFilter,
    ProjectPaginated,
    ProjectPatch,
    ProjectResponse,
)
from src.types import T_ADMIN
from src.utils import (
    create_audit,
    get_filter_clause,
    get_update_clause,
    tuple_to_pydantic,
)

router = APIRouter(
    prefix="/project",
    tags=["project"],
)


@router.get(
    "/",
    response_model=ProjectPaginated,
)
async def get_projects(
    current_user: T_ADMIN,
    pagination: Annotated[Pagination, Depends()],
    filter_input: Annotated[ProjectFilter, Depends()],
):
    sql: str = """
        SELECT
            id, created_at, updated_at,
            name, description
        FROM
            tbl_project
    """

    filter_data: dict = filter_input.get_data(filter_input)
    if filter_data:
        sql += get_filter_clause(filter_data)

    cur = conn.cursor()
    res_projects = cur.execute(sql, tuple(filter_data.values()))
    res_projects: list[tuple | None] = res_projects.fetchmany(
        pagination.per_page,
    )
    data: list[ProjectResponse] = [
        tuple_to_pydantic(ProjectResponse, project)
        for project in res_projects
    ]
    return ProjectPaginated(data=data, pagination=pagination)


@router.get(
    "/id={project_id}",
    response_model=ProjectResponse,
)
async def get_project_by_id(
    current_user: T_ADMIN,
    project_id: int,
):
    sql: str = """
        SELECT
            id, created_at, updated_at,
            name, description
        FROM
            tbl_project
        WHERE
            id = ?
    """

    cur = conn.cursor()
    res_project = cur.execute(sql, (project_id,))
    res_project: tuple | None = res_project.fetchone()
    if res_project is None:
        raise EXC_RES_NOT_FOUND
    return tuple_to_pydantic(ProjectResponse, res_project)


@router.post(
    "/",
    response_model=ProjectResponse,
)
async def create_project(
    current_user: T_ADMIN,
    create_data: Annotated[ProjectCreate, Depends()],
    bg_tasks: BackgroundTasks,
):
    data: dict = create_data.model_dump()

    sql: str = """
        INSERT INTO tbl_project(
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
            "tbl_project",
            AuditAction.CREATE.value,
            f"Created project: {create_data.name}",
            datetime.now(tz=UTC)
        )
    )

    sql = """
        SELECT
            id, created_at, updated_at,
            name, description
        FROM
            tbl_project
        WHERE
            id = ?
    """
    res = cur.execute(sql, (res.lastrowid,))
    res = cur.fetchone()
    return tuple_to_pydantic(ProjectResponse, res)


@router.patch(
    "/{project_id}",
    response_class=Response,
)
async def patch_project_by_id(
    current_user: T_ADMIN,
    project_id: int,
    patch_data: Annotated[ProjectPatch, Depends()],
    bg_tasks: BackgroundTasks,
):
    cur = conn.cursor()
    res_project = cur.execute(
        "SELECT id FROM tbl_project WHERE id = ?",
        (project_id,),
    )
    res_project: tuple | None = res_project.fetchone()
    if res_project is None:
        raise EXC_RES_NOT_FOUND

    patch_data_d: dict = patch_data.model_dump(exclude_none=True)
    if not patch_data_d:
        return Response(status_code=status.HTTP_200_OK)

    sql: str = "UPDATE tbl_project"
    sql += get_update_clause(patch_data_d)
    sql += "WHERE id = ?;"

    cur = conn.cursor()
    res = cur.execute(sql, (*patch_data_d.values(), project_id))
    conn.commit()
    if res.rowcount == 0:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    bg_tasks.add_task(
        create_audit,
        (
            project_id,
            "tbl_project",
            AuditAction.UPDATE.value,
            f"Updated project: {project_id}",
            datetime.now(tz=UTC)
        )
    )

    return Response(status_code=status.HTTP_200_OK)


@router.delete(
    "/{project_id}",
    response_class=Response,
)
async def delete_project_by_id(
    current_user: T_ADMIN,
    project_id: int,
    bg_tasks: BackgroundTasks,
):
    cur = conn.cursor()
    res_project = cur.execute(
        "SELECT id FROM tbl_project WHERE id = ?",
        (project_id,),
    )
    res_project: tuple | None = res_project.fetchone()
    if res_project is None:
        raise EXC_RES_NOT_FOUND

    cur = conn.cursor()
    res = cur.execute("DELETE FROM tbl_project WHERE id = ?", (project_id,))
    conn.commit()
    if res.rowcount == 0:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    bg_tasks.add_task(
        create_audit,
        (
            project_id,
            "tbl_project",
            AuditAction.DELETE.value,
            "Deleted project",
            datetime.now(tz=UTC)
        )
    )
    return Response(status_code=status.HTTP_200_OK)
