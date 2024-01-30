from fastapi import APIRouter, status
from fastapi.responses import Response

from src.const import API_VERSION


router = APIRouter(
    prefix=API_VERSION,
    tags=["api"]
)


@router.get(
    "/health",
    response_class=Response,
)
def health():
    return Response(status_code=status.HTTP_200_OK)
