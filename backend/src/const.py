from fastapi import HTTPException, status

API_VERSION: str = "/v1"
DB_NAME: str = "sprout_exam.db"

EXC_INVALID_CREDS: HTTPException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect credentials",
)

EXC_TOKEN_EXPIRED: HTTPException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Expired token",
)

EXC_RES_NOT_FOUND: HTTPException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Resource not found",
)

EXC_RES_CREATE_FAILED: HTTPException = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Failed creating resource",
)
