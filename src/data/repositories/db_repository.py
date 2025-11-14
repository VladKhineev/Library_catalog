from src.core.database import AsyncSessionLocal
from src.core.decorators import handle_error
from src.data.models.book import BookORM
from src.api.schemas.book import Book, BookResponseDTO
from src.data.repositories.base_repository import BaseBookRepository
from sqlalchemy import select


class DBBookRepository(BaseBookRepository):
    def __init__(self, session_factory, logger_instance=None):
        super().__init__(logger_instance)
        self.logger.info("POSTGRES DB")

        self.session_factory = session_factory

    @handle_error()
    async def get_books(self):
        async with self.session_factory() as session:
            result = await session.scalars(select(BookORM).order_by(BookORM.id))
            orm_books = result.all()  # теперь это list[BookORM]
            # Конвертация в Pydantic-схему
            return [
                {k: v for k, v in book.__dict__.items() if k != "_sa_instance_state"}
                for book in orm_books
            ]

    @handle_error()
    async def add_book(self, book) -> BookResponseDTO:
        async with self.session_factory() as session:
            db_book = BookORM(**book.model_dump())
            session.add(db_book)
            await session.commit()
            await session.refresh(db_book)
            return BookResponseDTO.model_validate(db_book.__dict__)

    @handle_error()
    async def get_book(self, book_id) -> BookResponseDTO | None:
        async with self.session_factory() as session:
            book = await session.get(BookORM, book_id)
            return Book.model_validate(book.__dict__) if book else None

    @handle_error()
    async def update_book(self, book: Book) -> BookResponseDTO | None:
        async with self.session_factory() as session:
            db_book = await session.get(BookORM, book.id)
            if not db_book:
                return None
            for field, value in book.model_dump().items():
                setattr(db_book, field, value)
            await session.commit()
            await session.refresh(db_book)
            return BookResponseDTO.model_validate(db_book.__dict__)

    @handle_error()
    async def delete_book(self, book_id: int) -> BookResponseDTO | None:
        async with self.session_factory() as session:
            db_book = await session.get(BookORM, book_id)
            if not db_book:
                return None
            await session.delete(db_book)
            await session.commit()
            return BookResponseDTO.model_validate(db_book.__dict__)

