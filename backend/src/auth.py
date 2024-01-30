from datetime import datetime, timedelta, UTC

from fastapi import HTTPException, status
from jose import ExpiredSignatureError, JWTError, jwt

from src.context import pwd
from src.db import conn
from src.enums import TokenType
from src.models.user import UserDB
from src.utils import tuple_to_pydantic
from src.settings import settings


async def authenticate_user(email: str, password: str) -> UserDB:
    cur = conn.cursor()
    res_user = cur.execute(
        "SELECT * FROM tbl_employee WHERE email = ?",
        (email,),
    )
    res_user: tuple = res_user.fetchone()

    if res_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="Incorrect credentials",
        )

    user: UserDB = tuple_to_pydantic(UserDB, res_user)
    if not pwd.verify(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="Incorrect credentials",
        )

    return user


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
