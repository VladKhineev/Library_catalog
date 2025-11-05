import loguru

from src.models.book_model import Book
from src.repositories.base_repository import BaseBookRepository


class BookManager:
    def __init__(self, repository: BaseBookRepository, logger=None):
        self.repository = repository
        self.logger = logger or loguru.logger

    async def get_books(self):
        self.logger.info("Получаем все книги")

        return await self.repository.get_books()

    async def add_book(self, book: Book):
        self.logger.info(f"Добавляем книгу: {book.title}")

        book = await self.repository.add_book(book)
        self.logger.info(f"✅ Книга '{book.title}' успешно добавлена.")
        return book

    async def get_book(self, book_id: int):
        self.logger.info(f"Получаем книгу ID={book_id}")

        book = await self.repository.get_book(book_id)
        return book

    async def update_book(self, new_book: Book):
        self.logger.info(f"Обновляем книгу ID={new_book.id}")

        book = await self.repository.update_book(new_book)
        self.logger.info(f"✅ Книга '{book.title}' успешно обновлена.")
        return book

    async def delete_book(self, book_id: int):
        self.logger.info(f"Удаляем книгу ID={book_id}")

        book = await self.repository.delete_book(book_id)
        self.logger.info(f"✅ Книга '{book.title}' успешно удалена.")
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
