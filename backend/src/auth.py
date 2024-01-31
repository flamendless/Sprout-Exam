from datetime import UTC, datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from jose import ExpiredSignatureError, JWTError, jwt

from src.const import EXC_INVALID_CREDS, EXC_TOKEN_EXPIRED
from src.context import oauth2_scheme, pwd
from src.db import conn
from src.enums import EmployeeType, TokenType
from src.models.employee import EmployeeDB
from src.models.jwt import TokenData
from src.settings import settings
from src.utils import is_value_in_enum, tuple_to_pydantic


def get_user(email: str) -> EmployeeDB | None:
    cur = conn.cursor()
    res_user = cur.execute(
        """
            SELECT
                id, created_at, updated_at,
                email, password, first_name,
                last_name, type, number_of_leaves
            FROM
                tbl_employee
            WHERE
                email = ?
        """,
        (email,),
    )
    res_user: tuple = res_user.fetchone()
    if res_user is None:
        return None
    employee: EmployeeDB = tuple_to_pydantic(EmployeeDB, res_user)
    return employee


async def authenticate_user(email: str, password: str) -> EmployeeDB:
    employee: EmployeeDB = get_user(email)

    if employee is None:
        raise EXC_INVALID_CREDS

    if not pwd.verify(password, employee.password):
        raise EXC_INVALID_CREDS

    return employee


def create_access_token(
    token_type: TokenType,
    data: dict,
    expires_delta: timedelta | None = None,
) -> str:
    to_encode = data.copy()
    utc_now = datetime.now(tz=UTC)
    expire = None
    if expires_delta:
        expire = utc_now + expires_delta
    else:
        expire = utc_now + timedelta(minutes=15)

    to_encode.update({
        "exp": expire,
        "token_type": token_type,
    })
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm,
    )
    return encoded_jwt


def validate_refresh_token(token: str) -> dict:
    payload = jwt.decode(
        token,
        settings.secret_key,
        algorithms=[settings.algorithm],
    )

    token_type: TokenType = payload.get("token_type")
    if (token_type is None) or (token_type != TokenType.REFRESH):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="Incorrect credentials",
        )

    if not payload.get("sub"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="Incorrect credentials",
        )

    return payload


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> EmployeeDB:
    token_data: TokenData | None = None
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )

        token_type: TokenType = payload.get("token_type")
        if (
            (token_type is None) or
            (not is_value_in_enum(TokenType, token_type))
        ):
            raise EXC_INVALID_CREDS

        username: str = payload.get("sub")
        if username is None:
            raise EXC_INVALID_CREDS

        token_data = TokenData(username=username)

    except ExpiredSignatureError as exc:
        raise EXC_TOKEN_EXPIRED from exc

    except JWTError as exc:
        raise EXC_INVALID_CREDS from exc

    user = get_user(email=token_data.username)
    if user is None:
        raise EXC_INVALID_CREDS

    return user


def get_current_employee_by_type(
    employee_type: EmployeeType,
) -> EmployeeDB | None:
    async def wrapped(
        current_user: Annotated[EmployeeDB, Depends(get_current_user)],
    ):
        if current_user.type != employee_type:
            raise EXC_INVALID_CREDS
        return current_user
    return wrapped
