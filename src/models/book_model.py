from pydantic import BaseModel
from enum import Enum


class AvailabilityStatus(str, Enum):
    IN_STOCK = 'в наличии'
    ISSUED= 'выдана'

class BookExternalInfo(BaseModel):
    cover: str | None = None
    description: str | None = None

class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int
    genre: str
    count_page: int
    accessibility: AvailabilityStatus
    external: BookExternalInfo | None = None

