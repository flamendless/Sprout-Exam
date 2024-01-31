from typing import Annotated

from fastapi import Depends

from src.auth import get_current_employee_by_type, get_current_user
from src.enums import EmployeeType
from src.models.employee import EmployeeDB

T_CURRENT_USER = Annotated[EmployeeDB, Depends(get_current_user)]
T_ADMIN = Annotated[
    EmployeeDB,
    Depends(get_current_employee_by_type(EmployeeType.ADMIN)),
]
