from http.client import responses

from fastapi import HTTPException
import os
import httpx
from fastapi_cloud_cli.utils.cli import handle_http_errors

import src.models as models

class JsonBin:
    """
    Класс для работы с API JSONBin.io (CRUD)
    """
    INDEX_BIN_ID = "6722b1ff8a8c444e3b99b123"
    BASE_URL = "https://api.jsonbin.io/v3/b"

    def __init__(self, master_key: str = None, bin_id: str = None):
        """
        Инициализация клиента JSONBin
        :param master_key: Секретный ключ из JSONBin.io
        :param index_bin_id: Bin со всеми данными
        """
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


    def get_books(self) -> list[dict]:
        response = httpx.get(self.url, headers=self.headers)
        return response.json()['record']['bins']

    def get_book(self, book_id: int) -> list[dict]:
        books = self.get_books()
        res = {}
        for book in books:
            if book_id == book['id']:
                res = book
        return res

    def add_book(self, book: models.Book) -> list[dict]:
        books: list[dict] = self.get_books()
        books.append(book.model_dump())
        res = {
            'bins': books
        }
        response = httpx.put(self.url, json=res, headers=self.headers)
        return response.json()['record']['bins']

    def update_book(self, new_book: models.Book) -> list[dict]:
        self.delete_book(new_book.id)
        res = self.add_book(new_book)
        return res

    def delete_book(self, book_id: int) -> list[dict]:
        books: list[dict] = self.get_books()
        for i, book in enumerate(books):
            if book_id == book['id']:
                books.pop(i)
        res = {
            'bins': books
        }
        response = httpx.put(self.url, json=res, headers=self.headers)
        return response.json()['record']['bins']

if __name__ == '__main__':
    book = models.Book(**{
        "id": 1,
        "title": "Sasha",
        "autor": "string",
        "year": 100,
        "genre": "string",
        "count_page": 0,
        "accessibility": "в наличии"
    })

    js = JsonBin('$2a$10$v/qfQsVRSLYVUUe7wBPp5ONexSDmwvuqchMBwBZzEDSJErk24DW4O', '69008a2a43b1c97be986cdc7')
    print(js.update_book(book))
