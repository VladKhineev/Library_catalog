from http.client import responses

from fastapi import HTTPException
import os
import httpx
from fastapi_cloud_cli.utils.cli import handle_http_errors

from src.models.book_model import Book
from src.repositories.base_repository import BaseBookRepository

from src.core.decorators import handle_error
import src.core.exceptions as exception

class JsonBinRepository(BaseBookRepository):
    """
    Класс для работы с API JSONBin.io (CRUD)
    """
    INDEX_BIN_ID = "6722b1ff8a8c444e3b99b123"
    BASE_URL = "https://api.jsonbin.io/v3/b"

    def __init__(self, master_key: str = None, bin_id: str = None, logger_instance=None):
        """
        Инициализация клиента JSONBin
        :param master_key: Секретный ключ из JSONBin.io
        :param bin_id: Bin со всеми данными
        :param logger_instance: logger
        """
        super().__init__(logger_instance)
        self.logger.info(f"JSON BIN")

        self.master_key = master_key or os.getenv("JSONBIN_SECRET_KEY")
        if not self.master_key:
            raise ValueError("Не указан JSONBIN_SECRET_KEY")

        self.headers = {
            "Content-Type": "application/json",
            "X-Master-Key": self.master_key,
        }

        self.bin_id = bin_id
        if not self.bin_id :
            raise ValueError("Не указан bin_id")

        self.url = f"{self.BASE_URL}/{bin_id}"


    @handle_error()
    def get_books(self) -> list[dict]:
        response = httpx.get(self.url, headers=self.headers)
        return response.json()['record']['bins']

    @handle_error()
    def add_book(self, book):
        books: list[dict] = self.get_books()
        books.append(book.model_dump())
        res = {
            'bins': books
        }
        response = httpx.put(self.url, json=res, headers=self.headers)
        return book

    @handle_error()
    def get_book(self, book_id):
        books: list[dict] = self.get_books()
        for book in books:
            if book_id == book['id']:
                return Book(**book)
        raise exception.BookNotFoundError(f"Книга '{book_id}' не найдена")

    @handle_error()
    def update_book(self, new_book):
        self.delete_book(new_book.id)
        self.add_book(new_book)
        return new_book

    @handle_error()
    def delete_book(self, book_id):
        books: list[dict] = self.get_books()
        deleted_book = None
        for i, book in enumerate(books):
            if book_id == book['id']:
                deleted_book = books.pop(i)
        if not deleted_book:
            raise exception.BookNotFoundError(f"Книга '{book_id}' не найдена")
        res = {
            'bins': books
        }
        response = httpx.put(self.url, json=res, headers=self.headers)
        return deleted_book

if __name__ == '__main__':
    book = Book(**{
        "id": 1,
        "title": "Sasha",
        "autor": "string",
        "year": 100,
        "genre": "string",
        "count_page": 0,
        "accessibility": "в наличии"
    })
