from datetime import UTC, datetime

import pytest

from fastapi import status
from httpx import AsyncClient

from src.const import API_VERSION
from src.db import create_admin, new_conn
from src.enums import EmployeeType
from src.tests.utils import basic_dt_comp, get_admin_token


EMPLOYEE_IDS: list[int] = []
BENEFIT_IDS: list[int] = []
PROJECT_IDS: list[int] = []


@pytest.mark.anyio
async def test_create_admin(client: AsyncClient) -> None:
    create_admin()
    cur = new_conn().cursor()
    res = cur.execute(
        "SELECT id FROM tbl_employee WHERE type = ?;",
        (EmployeeType.ADMIN.value,),
    )
    res: tuple = res.fetchone()
    assert res is not None


@pytest.mark.anyio
async def test_create_employees(client: AsyncClient) -> None:
    access_token: str = await get_admin_token(client)
    data: list[dict] = [
        {
            "email": "email3@test.com",
            "first_name": "fname",
            "last_name": "lname",
            "password": "TestPassword123!?",
            "type": EmployeeType.REGULAR,
            "number_of_leaves": 5,
            "contract_end_date": None,
        },
        {
            "email": "email4@test.com",
            "first_name": "fname",
            "last_name": "lname",
            "password": "TestPassword123!?",
            "type": EmployeeType.CONTRACTUAL,
            "number_of_leaves": None,
            "contract_end_date": str(datetime.now(tz=UTC)),
        },
    ]

    for d in data:
        res = await client.post(
            f"{API_VERSION}/employee/",
            headers={"Authorization": f"Bearer {access_token}"},
            json=d,
        )
        assert res.status_code == status.HTTP_200_OK, res.read()

        res_data: dict = res.json()
        assert res_data["id"]
        assert res_data["email"] == d["email"]
        assert "password" not in res_data
        assert res_data["first_name"] == d["first_name"]
        assert res_data["last_name"] == d["last_name"]
        assert res_data["type"] == d["type"]
        assert res_data["number_of_leaves"] == d["number_of_leaves"]
        if res_data["type"] == EmployeeType.CONTRACTUAL.value:
            assert basic_dt_comp(
                res_data["contract_end_date"],
                d["contract_end_date"],
            )
        else:
            assert res_data["contract_end_date"] == d["contract_end_date"]
        assert res_data["created_at"]
        assert res_data["updated_at"]
        EMPLOYEE_IDS.append(res_data["id"])

    assert len(EMPLOYEE_IDS) == len(data)


@pytest.mark.anyio
async def test_create_benefits(client: AsyncClient) -> None:
    access_token: str = await get_admin_token(client)
    data: list[dict] = [
        {
            "name": "Benefit 3",
            "description": "awesome benefit 1",
        },
        {
            "name": "Benefit 4",
            "description": "awesome benefit 2",
        },
    ]

    for d in data:
        res = await client.post(
            f"{API_VERSION}/benefit/",
            headers={"Authorization": f"Bearer {access_token}"},
            json=d,
        )
        assert res.status_code == status.HTTP_200_OK, res.read()

        res_data: dict = res.json()
        assert res_data["id"]
        assert res_data["name"] == d["name"]
        assert res_data["description"] == d["description"]
        assert res_data["created_at"]
        assert res_data["updated_at"]
        BENEFIT_IDS.append(res_data["id"])

    assert len(BENEFIT_IDS) == len(data)


@pytest.mark.anyio
async def test_create_projects(client: AsyncClient) -> None:
    access_token: str = await get_admin_token(client)
    data: list[dict] = [
        {
            "name": "Project 3",
            "description": "awesome project 1",
        },
        {
            "name": "Project 4",
            "description": "awesome project 2",
        },
    ]

    for d in data:
        res = await client.post(
            f"{API_VERSION}/project/",
            headers={"Authorization": f"Bearer {access_token}"},
            json=d,
        )
        assert res.status_code == status.HTTP_200_OK, res.read()

        res_data: dict = res.json()
        assert res_data["id"]
        assert res_data["name"] == d["name"]
        assert res_data["description"] == d["description"]
        assert res_data["created_at"]
        assert res_data["updated_at"]
        PROJECT_IDS.append(res_data["id"])

    assert len(PROJECT_IDS) == len(data)


@pytest.mark.anyio
async def test_assign_benefits(client: AsyncClient) -> None:
    access_token: str = await get_admin_token(client)
    for benefit_id in BENEFIT_IDS:
        res = await client.post(
            f"{API_VERSION}/benefit/{benefit_id}/assign",
            headers={"Authorization": f"Bearer {access_token}"},
            json=EMPLOYEE_IDS,
        )
        assert res.status_code == status.HTTP_200_OK, res.read()


@pytest.mark.anyio
async def test_assign_project(client: AsyncClient) -> None:
    access_token: str = await get_admin_token(client)
    for project_id in PROJECT_IDS:
        res = await client.post(
            f"{API_VERSION}/project/{project_id}/assign",
            headers={"Authorization": f"Bearer {access_token}"},
            json=EMPLOYEE_IDS,
        )
        assert res.status_code == status.HTTP_200_OK, res.read()
