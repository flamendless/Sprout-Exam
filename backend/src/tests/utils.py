from fastapi import status
from httpx import AsyncClient

from src.const import API_VERSION
from src.main import app


async def authentications(client: AsyncClient, prefix: str) -> None:
    routes_get: list[str] = []
    routes_post: list[str] = []
    routes_put: list[str] = []

    for route in app.routes:
        path: str = route.path
        if not path.startswith(prefix):
            continue
        method: str = list(route.methods)[0]
        match method:
            case "GET":
                routes_get.append(path)
            case "POST":
                routes_post.append(path)
            case "PUT":
                routes_put.append(path)

    for route in routes_get:
        res = await client.get(route)
        assert res.status_code == status.HTTP_401_UNAUTHORIZED, f"GET {route=}"

    for route in routes_post:
        res = await client.post(route)
        assert res.status_code == status.HTTP_401_UNAUTHORIZED, f"POST {route=}"

    for route in routes_put:
        res = await client.put(route)
        assert res.status_code == status.HTTP_401_UNAUTHORIZED, f"PUT {route=}"


async def get_admin_token(client: AsyncClient) -> str:
    res = await client.post(
        f"{API_VERSION}/auth/token",
        data={
            "grant_type": "password",
            "username": "admin@admin.com",
            "password": "admin",
        }
    )
    assert res.status_code == status.HTTP_200_OK, res.read()
    return res.json()["access_token"]


def basic_dt_comp(dt1: str, dt2: str) -> bool:
    return dt1[:10] == dt2[:10]
