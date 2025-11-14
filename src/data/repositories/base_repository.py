from abc import ABC, abstractmethod

from loguru import logger

from src.api.schemas.book import Book, BookResponseDTO, BookUpdateDTO


class BaseBookRepository[T: BookResponseDTO](ABC):
    """Абстрактный репозиторий для работы с книгами."""

    def __init__(self, logger_instance=None):
        self.logger = logger_instance or logger

    @abstractmethod
    def get_books(self) -> list[dict]:
        pass

    @abstractmethod
    def add_book(self, book: Book) -> T:
        pass

    @abstractmethod
    def get_book(self, book_id: int) -> T:
        pass

    @abstractmethod
    def update_book(self, new_book: BookUpdateDTO) -> T:
        pass

    @abstractmethod
    def delete_book(self, book_id: int) -> T:
        pass
