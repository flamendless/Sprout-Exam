import pytest
from fastapi import status
from httpx import AsyncClient

from src.const import API_VERSION
from src.db import create_admin, new_conn
from src.enums import EmployeeType
from src.tests.utils import authentications, get_admin_token


IDS: list[int] = []


@pytest.mark.anyio
async def test_projects_auths(client: AsyncClient) -> None:
    await authentications(client, f"{API_VERSION}/project/")


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
async def test_create_projects(client: AsyncClient) -> None:
    access_token: str = await get_admin_token(client)
    data: list[dict] = [
        {
            "name": "Project 1",
            "description": "awesome project 1",
        },
        {
            "name": "Project 2",
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
        IDS.append(res_data["id"])

    assert len(IDS) == len(data)


@pytest.mark.anyio
async def test_get_projects_by_id(client: AsyncClient) -> None:
    access_token: str = await get_admin_token(client)
    for project_id in IDS:
        res = await client.get(
            f"{API_VERSION}/project/{project_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert res.status_code == status.HTTP_200_OK, res.read()
        res_data: dict = res.json()
        assert res_data["id"] == project_id


@pytest.mark.anyio
async def test_update_projects(client: AsyncClient) -> None:
    access_token: str = await get_admin_token(client)
    patch: dict[str, str] = {"description": "updated description"}
    for project_id in IDS:
        res = await client.patch(
            f"{API_VERSION}/project/{project_id}",
            headers={"Authorization": f"Bearer {access_token}"},
            json=patch,
        )
        assert res.status_code == status.HTTP_200_OK, res.read()

        res2 = await client.get(
            f"{API_VERSION}/project/{project_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert res2.status_code == status.HTTP_200_OK, res2.read()

        res_data: dict = res2.json()
        assert res_data["id"] == project_id
        assert res_data["name"]
        assert res_data["description"] == patch["description"]
        assert res_data["created_at"]
        assert res_data["updated_at"]


@pytest.mark.anyio
async def test_delete_projects(client: AsyncClient) -> None:
    access_token: str = await get_admin_token(client)
    for project_id in IDS:
        res = await client.delete(
            f"{API_VERSION}/project/{project_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert res.status_code == status.HTTP_200_OK, res.read()

        res2 = await client.get(
            f"{API_VERSION}/project/{project_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert res2.status_code == status.HTTP_404_NOT_FOUND, res2.read()
