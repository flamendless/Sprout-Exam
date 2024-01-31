from pydantic import BaseModel

from src.enums import EmployeeType, TokenType


class Token(BaseModel):
    access_token: str
    token_type: TokenType
    expires_in: int
    refresh_token: str
    type: EmployeeType


class TokenData(BaseModel):
    username: str
