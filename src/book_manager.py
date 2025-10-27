from operator import index

import src.models as models
from src.db_manager import DBBookRepository
from src.json_manager import JsonBookManager


class BookManager:
    def __init__(self, index_repository):
        if index_repository == 'db':
            self.repository = DBBookRepository('postgresql://postgres:postgres@localhost:5432/Library')
        elif index_repository == 'json':
            self.repository = JsonBookManager()

    def add_book(self, book: models.Book):
        return self.repository.add_book(book)

    def get_books(self):
        return self.repository.get_books()

    def get_book(self, book_id: int):
        return self.repository.get_book(book_id)

    def update_book(self, new_book: models.Book):
        return self.repository.update_book(new_book)

    def delete_book(self, book_id: int):
        return self.repository.delete_book(book_id)

if __name__ == '__main__':
    book = models.Book(**{
        "id": 4,
        "title": "Sasha",
        "autor": "string",
        "year": 0,
        "genre": "string",
        "count_page": 1000000000,
        "accessibility": "в наличии"
    })
    bm = BookManager('json')
    print(bm.get_books())
