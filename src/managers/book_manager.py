from src.schemas.book_model import Book, BookCreateDTO, BookUpdateDTO
from src.repositories.base_repository import BaseBookRepository


class BookManager:
    def __init__(self, repository: BaseBookRepository):
        self.repository = repository

    async def get_books(self):
        return await self.repository.get_books()

    async def add_book(self, book: Book):
        new_book = await self.repository.add_book(book)

        return new_book

    async def get_book(self, book_id: int):
        book = await self.repository.get_book(book_id)

        return book

    async def update_book(self, new_book: BookUpdateDTO):
        book = await self.repository.update_book(new_book)

        return book

    async def delete_book(self, book_id: int):
        book = await self.repository.delete_book(book_id)

        return book


if __name__ == '__main__':
    book = Book(
        **{
            "id": 4,
            "title": "Sasha",
            "author": "string",
            "year": 0,
            "genre": "string",
            "count_page": 1000000000,
            "accessibility": "в наличии",
        }
    )
    bm = BookManager('bin')
    print(bm.get_books())
