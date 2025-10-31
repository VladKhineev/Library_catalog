from abc import ABC, abstractmethod

from loguru import logger

from src.models.book_model import Book


class BaseBookRepository(ABC):
    """Абстрактный репозиторий для работы с книгами."""

    def __init__(self, logger_instance=None):
        self.logger = logger_instance or logger

    @abstractmethod
    def get_books(self) -> list[Book]:
        pass

    @abstractmethod
    def add_book(self, book: Book) -> Book:
        pass

    @abstractmethod
    def get_book(self, book_id: int) -> Book:
        pass

    @abstractmethod
    def update_book(self, new_book: Book) -> Book:
        pass

    @abstractmethod
    def delete_book(self, book_id: int) -> Book:
        pass
