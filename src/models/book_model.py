from enum import Enum

from pydantic import BaseModel, Field, field_validator


class AvailabilityStatus(str, Enum):
    IN_STOCK = 'в наличии'
    ISSUED = 'выдана'


class BookExternalInfo(BaseModel):
    cover: str | None = None
    description: str | None = None


class Book(BaseModel):
    id: int = Field(gt=0)
    title: str = Field(min_length=1, max_length=255)
    author: str = Field(min_length=1, max_length=255)
    year: int = Field(ge=1000, le=2100)
    genre: str = Field(min_length=1, max_length=100)
    page_count: int = Field(gt=0, alias="count_page")
    availability: AvailabilityStatus
    external: BookExternalInfo | None = None

    @field_validator('year')
    @classmethod
    def validate_year(cls, v):
        from datetime import datetime
        if v > datetime.now().year + 10:
            raise ValueError('Year too far in future')
        return v
