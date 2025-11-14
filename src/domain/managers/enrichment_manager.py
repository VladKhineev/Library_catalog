from src.integrations.openlibrary_api import OpenLibraryAPI
from src.domain.managers.book_manager import BookManager
from src.api.schemas.book import Book, BookResponseDTO


class BookEnrichmentManager:
    def __init__(self, manager: BookManager, external_api: OpenLibraryAPI):
        self.manager = manager
        self.external_api = external_api

    async def add_with_api(self, book: Book) -> BookResponseDTO:
        book.external = await self.external_api.fetch_book_info(book.title)
        return await self.manager.add_book(book)


if __name__ == '__main__':
    pass
