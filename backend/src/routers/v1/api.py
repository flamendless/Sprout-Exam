from fastapi import APIRouter, status
from fastapi.responses import Response

router = APIRouter(
    prefix="/check",
    tags=["api"],
)


@router.get(
    "/health",
    response_class=Response,
)
def health():
    return Response(status_code=status.HTTP_200_OK)
