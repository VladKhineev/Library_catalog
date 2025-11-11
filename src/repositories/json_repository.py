import json
import os

import src.core.exceptions as exception
from src.core.decorators import handle_error
from src.models.book_model import Book
from src.repositories.base_repository import BaseBookRepository


class JsonBookRepository(BaseBookRepository):
    def __init__(self, logger_instance=None):
        super().__init__(logger_instance)
        self.logger.info("JSON ФАЙЛ")

        self.repo = JSONRepository('books.json')

    @handle_error()
    async def get_books(self):
        res = self.repo.load_data()
        return res

    @handle_error()
    async def add_book(self, book):
        books: list[dict] = await self.get_books()
        books.append(book.model_dump())
        self.repo.save_data(books)
        return book

    @handle_error()
    async def get_book(self, book_id):
        books: list[dict] = await self.get_books()
        for book in books:
            if book_id == book['id']:
                return Book(**book)
        raise exception.BookNotFoundError(f"Book '{book_id}' no found")

    @handle_error()
    async def update_book(self, new_book):
        deleted_book = await self.delete_book(new_book.id)
        if not deleted_book:
            raise AttributeError(f"Unable to update. Book '{new_book.id}' no found")
        await self.add_book(new_book)
        return new_book

    @handle_error()
    async def delete_book(self, book_id):
        books: list[dict] = await self.get_books()
        deleted_book = {}
        for i, book in enumerate(books):
            if book_id == book['id']:
                deleted_book = books.pop(i)
        self.repo.save_data(books)

        if not deleted_book:
            raise exception.BookNotFoundError(f"Book '{book_id}' no found")

        return Book(**deleted_book)


class JSONRepository:
    def __init__(self, filename: str):
        self.filename = filename

    def save_data(self, data: list[dict]):
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def load_data(self) -> list[dict]:
        if os.path.exists(self.filename):
            with open(self.filename, encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
        else:
            data = []

        return data


if __name__ == '__main__':
    book = Book(
        **{
            "id": 232,
            "title": "string",
            "author": "string",
            "year": 1,
            "genre": "string",
            "count_page": 0,
            "accessibility": "в наличии",
        }
    )
    jb = JsonBookRepository()
    jb.update_book(book)
