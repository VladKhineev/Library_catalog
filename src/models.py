from pydantic import BaseModel
from enum import Enum


class AvailabilityStatus(str, Enum):
    IN_STOCK = 'в наличии'
    ISSUED= 'выдана'

class Book(BaseModel):
    id: int
    title: str
    autor: str
    year: int
    genre: str
    count_page: int
    accessibility: AvailabilityStatus