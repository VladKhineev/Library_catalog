from abc import ABC, abstractmethod
from src.models.book_model import Book

class BaseBookRepository(ABC):

    @abstractmethod
    def get_books(self) -> list[Book]: pass

    @abstractmethod
    def add_book(self, book: Book) -> Book: pass

    @abstractmethod
    def get_book(self, book_id: int) -> Book: pass

    @abstractmethod
    def update_book(self, new_book: Book) -> Book: pass

    @abstractmethod
    def delete_book(self, book_id: int) -> Book: pass

