from src.models.book_model import Book
from src.repositories.base_repository import BaseBookRepository


class BookManager:
    def __init__(self, repository: BaseBookRepository):
        self.repository = repository

    def add_book(self, book: Book):
        return self.repository.add_book(book)

    def get_books(self):
        return self.repository.get_books()

    def get_book(self, book_id: int):
        return self.repository.get_book(book_id)

    def update_book(self, new_book: Book):
        return self.repository.update_book(new_book)

    def delete_book(self, book_id: int):
        return self.repository.delete_book(book_id)

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
