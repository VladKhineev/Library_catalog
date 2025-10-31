from src.integrations.openlibrary_api import OpenLibraryAPI
from src.managers.book_manager import BookManager
from src.models.book_model import Book


class BookEnrichmentManager:
    def __init__(self, manager: BookManager, external_api: OpenLibraryAPI):
        self.manager = manager
        self.external_api = external_api

    def add_with_api(self, book: Book):
        book.external = self.external_api.fetch_book_info(book.title)
        return self.manager.add_book(book)


if __name__ == '__main__':
    pass
