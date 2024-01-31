from pydantic import BaseModel, Field

from src.models.base import DB, Filter, Pagination


class BenefitDB(DB):
    name: str
    description: str


class BenefitResponse(BenefitDB):
    pass


class BenefitCreate(BaseModel):
    name: str
    description: str


class BenefitPatch(BaseModel):
    name: str | None = Field(default=None)
    description: str | None = Field(default=None)


class BenefitPaginated(BaseModel):
    data: list[BenefitResponse]
    pagination: Pagination


class BenefitFilter(Filter):
    id: int | None = Field(default=None)
    name: str | None = Field(default=None)
    description: str | None = Field(default=None)
