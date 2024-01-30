from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext


pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/token")
