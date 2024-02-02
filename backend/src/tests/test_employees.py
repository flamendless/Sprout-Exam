import pytest

from httpx import AsyncClient

from src.const import API_VERSION
from src.enums import EmployeeType
from src.tests.utils import authentications
from src.db import create_admin, new_conn


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
