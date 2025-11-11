from abc import ABC, abstractmethod

from loguru import logger

from src.models.book_model import Book, BookCreateDTO, BookResponseDTO, BookUpdateDTO


class BaseBookRepository(ABC):
    """Абстрактный репозиторий для работы с книгами."""

    def __init__(self, logger_instance=None):
        self.logger = logger_instance or logger

    @abstractmethod
    def get_books(self) -> list[dict]:
        pass

    @abstractmethod
    def add_book(self, book: Book) -> BookResponseDTO:
        pass

    @abstractmethod
    def get_book(self, book_id: int) -> BookResponseDTO:
        pass

    @abstractmethod
    def update_book(self, new_book: BookUpdateDTO) -> BookResponseDTO:
        pass

    @abstractmethod
    def delete_book(self, book_id: int) -> BookResponseDTO:
        pass
