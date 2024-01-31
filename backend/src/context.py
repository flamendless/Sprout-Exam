from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from src.const import API_VERSION

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{API_VERSION}/auth/token")
