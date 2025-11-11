import loguru
from src.managers.book_manager import BookManager
from src.managers.enrichment_manager import BookEnrichmentManager
from src.integrations.base_api_client import BaseApiClient
from src.models.book_model import Book, BookCreateDTO, BookResponseDTO, BookUpdateDTO

class BookService:
    def __init__(
        self,
        enrichment_api: BaseApiClient,
        manager: BookManager,
        enrichment_manager: BookEnrichmentManager,
        logger=None
    ):
        self.enrichment_api = enrichment_api
        self.manager = manager
        self.enrichment_manager = enrichment_manager
        self.logger = logger or loguru.logger

    async def get_id(self) -> int:
        list_books: list[BookResponseDTO] = await self.manager.get_books()

        if list_books:
            last_book = list_books[-1]
            return last_book['id'] + 1
        else:
            return 1


    async def get_list_books(self) -> list[BookResponseDTO]:
        self.logger.info("Get books")

        return await self.manager.get_books()

    async def create_book(self, create_book: BookCreateDTO) -> BookResponseDTO:
        self.logger.info("Book create", extra={"title": create_book.title})

        new_id = await self.get_id()
        book = Book(id=new_id, **create_book.model_dump())
        new_book = await self.manager.add_book(book)

        self.logger.info(
            "✅ Book created", extra={"book_id": new_book.id, "title": new_book.title}
        )

        return new_book


    async def get_book(self, book_id: int) -> BookResponseDTO:
        self.logger.info("Get book", extra={"book_id": book_id})

        book = await self.manager.get_book(book_id)

        self.logger.info(
            "✅ book received", extra={"book_id": book.id, "title": book.title}
        )

        return book

    async def update_book(self, new_book: BookUpdateDTO) -> BookResponseDTO:
        self.logger.info("Update book", extra={"book_id": new_book.id})

        updated_book = await self.manager.update_book(new_book)

        self.logger.info(
            "✅ Updated book", extra={"book_id": updated_book.id, "title": updated_book.title}
        )

        return updated_book

    async def delete_book(self, book_id: int) -> BookResponseDTO:
        self.logger.info("Delete book", extra={"book_id": book_id})

        deleted_book = await self.manager.delete_book(book_id)

        self.logger.info(
            "✅ Deleted book", extra={"book_id": deleted_book.id, "title": deleted_book.title}
        )

        return deleted_book

    async def add_with_api(self, create_book: BookCreateDTO) -> BookResponseDTO:
        self.logger.info("Book create with api", extra={"title": create_book.title})

        new_id = await self.get_id()
        book = Book(**create_book.model_dump(), id=new_id)
        book = await self.enrichment_manager.add_with_api(book)

        self.logger.info(
            "✅ Book created with api", extra={"book_id": book.id, "title": book.title}
        )

        return book