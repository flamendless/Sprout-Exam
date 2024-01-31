from datetime import datetime
from typing import Self

from pydantic import BaseModel, Field

from src.settings import settings


class DB(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime


class Pagination(BaseModel):
    page_no: int = Field(default=1)
    per_page: int = Field(
        default=settings.pagination_max_per_page,
        ge=1,
        le=settings.pagination_max_per_page,
    )
    has_next: bool = Field(default=False)
    has_prev: bool = Field(default=False)

    def get_skip(self) -> int:
        return (self.page_no - 1) * self.per_page

    async def populate_fields(
        self,
        filter_data: dict,
        skip: int,
    ) -> Self:
        # total: int = (
        #     await db_col(collection)
        #     .count_documents(filter_data, skip=skip)
        # )
        # self.has_next = total > self.per_page
        # self.has_prev = self.page_no > 1
        return self


class Filter(BaseModel):
    @staticmethod
    def get_data(data: Self) -> dict:
        return data.model_dump(exclude_none=True)
