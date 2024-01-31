from datetime import UTC, datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm

from src import auth
from src.enums import AuditAction, TokenType
from src.models.employee import EmployeeDB
from src.models.jwt import Token
from src.settings import settings
from src.utils import create_audit

router = APIRouter(
    prefix="/auth",
    tags=["jwt", "auth"],
)


@router.post(
    "/token",
    response_model=Token,
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    bg_tasks: BackgroundTasks,
):
    employee: EmployeeDB = await auth.authenticate_user(
        form_data.username,
        form_data.password
    )

    data: dict = {"sub": employee.email}
    access_token: str = auth.create_access_token(
        token_type=TokenType.ACCESS,
        data=data,
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
    )
    refresh_token: str = auth.create_access_token(
        token_type=TokenType.REFRESH,
        data=data,
        expires_delta=timedelta(minutes=settings.refresh_token_expire_minutes),
    )

    bg_tasks.add_task(
        create_audit,
        (
            employee.id,
            "tbl_employee",
            AuditAction.READ.value,
            "login",
            datetime.now(tz=UTC)
        )
    )

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.access_token_expire_minutes * 60,
        type=employee.type,
    )


@router.post(
    "/refresh",
    response_model=Token,
)
async def refresh_token(
    data: Annotated[str | None, Form()] = None
):
    payload: dict = auth.validate_refresh_token(data)
    new_data: dict = {"sub": payload.get("sub")}
    access_token: str = auth.create_access_token(
        token_type=TokenType.ACCESS,
        data=new_data,
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
    )
    refresh_token: str = auth.create_access_token(
        token_type=TokenType.REFRESH,
        data=new_data,
        expires_delta=timedelta(minutes=settings.refresh_token_expire_minutes),
    )
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.access_token_expire_minutes * 60,
    )
