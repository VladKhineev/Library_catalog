import loguru

from src.models.book_model import Book
from src.repositories.base_repository import BaseBookRepository


class BookManager:
    def __init__(self, repository: BaseBookRepository, logger=None):
        self.repository = repository
        self.logger = logger or loguru.logger

    def get_books(self):
        self.logger.info(f"Получаем все книги")
        return self.repository.get_books()

    def add_book(self, book: Book):
        self.logger.info(f"Добавляем книгу: {book.title}")
        try:
            book = self.repository.add_book(book)
            self.logger.info(f"✅ Книга '{book.title}' успешно добавлена.")
            return book
        except Exception as e:
            self.logger.exception(f"Ошибка при добавлении книги '{book.title}': {e}")
            raise

    def get_book(self, book_id: int):
        self.logger.info(f"Получаем книгу ID={book_id}")
        book = self.repository.get_book(book_id)
        if not book:
            self.logger.warning(f"❌ Книга с ID={book_id} не найдена.")
        return book

    def update_book(self, new_book: Book):
        self.logger.info(f"Обновляем книгу ID={new_book.id}")
        try:
            book = self.repository.update_book(new_book)
            self.logger.info(f"✅ Книга '{book.title}' успешно обновлена.")
            return book
        except Exception as e:
            self.logger.exception(f"Ошибка при обновлении книги '{new_book.title}': {e}")
            raise


    def delete_book(self, book_id: int):
        self.logger.info(f"Удаляем книгу ID={book_id}")
        try:
            book = self.repository.delete_book(book_id)
            if not book:
                self.logger.warning(f"❌ Книга с ID={book_id} не найдена.")

            self.logger.info(f"✅ Книга '{book.title}' успешно удалена.")
            return book
        except Exception as e:
            self.logger.exception(f"Ошибка при удалении книги '{book_id}': {e}")
            raise

if __name__ == '__main__':
    book = Book(**{
        "id": 4,
        "title": "Sasha",
        "autor": "string",
        "year": 0,
        "genre": "string",
        "count_page": 1000000000,
        "accessibility": "в наличии"
    })
    bm = BookManager('bin')
    print(bm.get_books())
