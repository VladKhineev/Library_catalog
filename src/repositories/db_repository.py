import asyncpg
from src.core.decorators import handle_error
from src.models.book_model import Book
from src.repositories.base_repository import BaseBookRepository


class DBBookRepository(BaseBookRepository):
    _pool: asyncpg.Pool | None = None

    def __init__(self, dsn: str = None, logger_instance=None):
        super().__init__(logger_instance)
        self.logger.info("POSTGRES DB")

        self.dsn = dsn

    async def _get_pool(self):
        if not DBBookRepository._pool:
            DBBookRepository._pool = await asyncpg.create_pool(
                dsn=self.dsn,
                min_size=5,
                max_size=20,
            )
        return DBBookRepository._pool

    # --------------------- TABLE MANAGEMENT --------------------- #

    async def create_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS books (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author VARCHAR(255),
            year INT,
            genre VARCHAR(100),
            count_page INT DEFAULT 0,
            accessibility VARCHAR(50) DEFAULT 'в наличии',
            external JSONB
        );
        '''
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            await conn.execute(query)

    async def drope_table(self):
        query = "DROP TABLE IF EXISTS books;"
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            await conn.execute(query)

    # ------------------------CRUD-----------------------------#

    @handle_error()
    async def get_books(self):
        query = "SELECT * FROM books ORDER BY id;"
        pool = await self._get_pool()

        async with pool.acquire() as conn:
            rows = await conn.fetch(query)
            return [Book(**book) for book in rows]


    @handle_error()
    async def add_book(self, book):
        query = """
                INSERT INTO books (title, author, year, genre, count_page, accessibility, external)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id;
                """
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            new_id = await conn.fetchval(
                query,
                book.title,
                book.author,
                book.year,
                book.genre,
                book.count_page,
                book.accessibility,
                book.external.model_dump_json(),
            )
            book.id = new_id
            return book


    @handle_error()
    async def get_book(self, book_id):
        query = "SELECT * FROM books WHERE id = %s;"
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            row = await conn.fetchrow(query, book_id)
            return Book(**dict(row)) if row else None


    @handle_error()
    async def update_book(self, new_book: Book) -> Book:
        query = """
               UPDATE books
               SET title = $1,
                   author = $2,
                   year = $3,
                   genre = $4,
                   count_page = $5,
                   accessibility = $6,
                   external = $7
               WHERE id = $8;
           """
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            await conn.execute(
                query,
                new_book.title,
                new_book.author,
                new_book.year,
                new_book.genre,
                new_book.count_page,
                new_book.accessibility,
                new_book.external.model_dump_json(),
                new_book.id,
            )
        return new_book


    @handle_error()
    async def delete_book(self, book_id: int) -> list[Book]:
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            await conn.execute("DELETE FROM books WHERE id = $1;", book_id)
        return await self.get_books()


if __name__ == '__main__':
    repo = DBBookRepository('postgresql://postgres:postgres@localhost:5432/Library')
    # repo.create_table()
    # repo.drope_table()
    print(repo.get_book(43242))
    # book = Book(**{
    #     "id": 5,
    #     "title": "Dima",
    #     "author": "string",
    #     "year": 0,
    #     "genre": "string",
    #     "count_page": 100,
    #     "accessibility": "в наличии"
    # })
    # print(repo.delete_book(5))
