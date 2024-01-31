from pydantic import BaseModel, Field

from src.models.base import DB, Filter, Pagination


class ProjectDB(DB):
    name: str
    description: str


class ProjectResponse(ProjectDB):
    pass


class ProjectCreate(BaseModel):
    name: str
    description: str


class ProjectPatch(BaseModel):
    name: str | None = Field(default=None)
    description: str | None = Field(default=None)


class ProjectPaginated(BaseModel):
    data: list[ProjectResponse]
    pagination: Pagination


class ProjectFilter(Filter):
    id: int | None = Field(default=None)
    name: str | None = Field(default=None)
    description: str | None = Field(default=None)
