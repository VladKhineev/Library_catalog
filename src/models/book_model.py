from enum import Enum

from pydantic import BaseModel, Field, field_validator

from datetime import datetime

class AccessibilityStatus(str, Enum):
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
    count_page: int = Field(gt=0, alias="count_page")
    accessibility: AccessibilityStatus
    external: BookExternalInfo | None = None

    @field_validator('year')
    @classmethod
    def validate_year(cls, v):
        from datetime import datetime
        if v > datetime.now().year + 10:
            raise ValueError('Year too far in future')
        return v

class BookCreateDTO(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    author: str = Field(min_length=1, max_length=255)
    year: int = Field(ge=1000, le=2100)
    genre: str = Field(min_length=1, max_length=100)
    count_page: int = Field(gt=0, alias="count_page")
    accessibility: AccessibilityStatus

class BookUpdateDTO(BaseModel):
    id: int = Field(gt=0)
    title: str | None = Field(min_length=1, max_length=255, default=None)
    author: str | None = Field(min_length=1, max_length=255, default=None)
    year: int | None = Field(ge=1000, le=2100, default=None)
    genre: str | None = Field(min_length=1, max_length=100, default=None)
    count_page: int | None = Field(gt=0, alias="count_page", default=None)
    accessibility: AccessibilityStatus
    external: BookExternalInfo | None = None

class BookResponseDTO(BaseModel):
    id: int = Field(gt=0)
    title: str = Field(min_length=1, max_length=255)
    author: str = Field(min_length=1, max_length=255)
    year: int = Field(ge=1000, le=2100)
    genre: str = Field(min_length=1, max_length=100)
    count_page: int = Field(gt=0, alias="count_page")
    accessibility: AccessibilityStatus
    external: BookExternalInfo | None = None
