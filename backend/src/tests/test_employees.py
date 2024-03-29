from datetime import UTC, datetime

import pytest
from fastapi import status
from httpx import AsyncClient

from src.const import API_VERSION
from src.db import create_admin, new_conn
from src.enums import EmployeeType
from src.tests.utils import authentications, basic_dt_comp, get_admin_token


IDS: list[int] = []


@pytest.mark.anyio
async def test_employees_auths(client: AsyncClient) -> None:
    await authentications(client, f"{API_VERSION}/employee/")


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
            "email": "email@test.com",
            "first_name": "fname",
            "last_name": "lname",
            "password": "TestPassword123!?",
            "type": EmployeeType.REGULAR,
            "number_of_leaves": 5,
            "contract_end_date": None,
        },
        {
            "email": "email2@test.com",
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
        IDS.append(res_data["id"])

    assert len(IDS) == len(data)


@pytest.mark.anyio
async def test_get_employees_by_id(client: AsyncClient) -> None:
    access_token: str = await get_admin_token(client)
    for employee_id in IDS:
        res = await client.get(
            f"{API_VERSION}/employee/{employee_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert res.status_code == status.HTTP_200_OK, res.read()
        res_data: dict = res.json()
        assert res_data["id"] == employee_id
        assert "password" not in res_data


@pytest.mark.anyio
async def test_update_employees(client: AsyncClient) -> None:
    access_token: str = await get_admin_token(client)
    patch: dict[str, str] = {
        "first_name": "updated first name",
        "last_name": "updated last name",
    }
    for employee_id in IDS:
        res = await client.patch(
            f"{API_VERSION}/employee/{employee_id}",
            headers={"Authorization": f"Bearer {access_token}"},
            json=patch,
        )
        assert res.status_code == status.HTTP_200_OK, res.read()

        res2 = await client.get(
            f"{API_VERSION}/employee/{employee_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert res2.status_code == status.HTTP_200_OK, res2.read()

        res_data: dict = res2.json()
        assert res_data["id"] == employee_id
        assert "password" not in res_data
        assert res_data["first_name"] == patch["first_name"]
        assert res_data["last_name"] == patch["last_name"]
        assert res_data["created_at"]
        assert res_data["updated_at"]


@pytest.mark.anyio
async def test_delete_employees(client: AsyncClient) -> None:
    access_token: str = await get_admin_token(client)
    for employee_id in IDS:
        res = await client.delete(
            f"{API_VERSION}/employee/{employee_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert res.status_code == status.HTTP_200_OK, res.read()

        res2 = await client.get(
            f"{API_VERSION}/employee/{employee_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert res2.status_code == status.HTTP_404_NOT_FOUND, res2.read()
