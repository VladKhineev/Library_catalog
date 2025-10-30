import psycopg2
from psycopg2.extras import RealDictCursor, RealDictRow

from src.models.book_model import Book, BookExternalInfo
from src.repositories.base_repository import BaseBookRepository

from src.core.decorators import handle_error
import src.core.exceptions as exception

class DBBookRepository(BaseBookRepository):
    def __init__(self, dns: str = None, logger_instance=None):
        super().__init__(logger_instance)
        self.logger.info(f"POSTGRES DB")

        self.dns = dns

    def _get_connection(self):
        return psycopg2.connect(self.dns)

    def create_table(self):
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
        with self._get_connection() as conn, conn.cursor() as cur:
            cur.execute(query)
            conn.commit()

    def drope_table(self):
        query = '''
        DROP TABLE books;
        '''
        with self._get_connection() as conn, conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
    #------------------------CRUD-----------------------------#

    @handle_error()
    def get_books(self):
        query = "SELECT * FROM books ORDER BY id;"
        with self._get_connection() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            list_books = cur.fetchall()
            res = [Book(**book) for book in list_books]
            return res

    @handle_error()
    def add_book(self, book):
        query = """
                INSERT INTO books (title, author, year, genre, count_page, accessibility, external)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id;
                """
        with self._get_connection() as conn, conn.cursor() as cur:
            cur.execute(query, (
                book.title,
                book.author,
                book.year,
                book.genre,
                book.count_page,
                book.accessibility,
                book.external.model_dump_json(),
            ))
            book_id = cur.fetchone()[0]
            conn.commit()
            return book

    @handle_error()
    def get_book(self, book_id):
        query = "SELECT * FROM books WHERE id = %s;"
        with self._get_connection() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (book_id,))
            res = Book(**cur.fetchone())
            return res

    @handle_error()
    def update_book(self, new_book):
        query = """
                UPDATE books
                SET title = %s,
                    author = %s,
                    year = %s,
                    genre = %s,
                    count_page = %s,
                    accessibility = %s,
                    external = %s
                WHERE id = %s;
                """
        with self._get_connection() as conn, conn.cursor() as cur:
            cur.execute(query, (
                new_book.title,
                new_book.author,
                new_book.year,
                new_book.genre,
                new_book.count_page,
                new_book.accessibility,
                new_book.external.model_dump_json(),
                new_book.id,
            ))
            conn.commit()

        return new_book


    @handle_error()
    def delete_book(self, book_id) -> list[Book]:
        query = "DELETE FROM books WHERE id = %s;"
        with self._get_connection() as conn, conn.cursor() as cur:
            cur.execute(query, (book_id,))
            conn.commit()

        return self.get_books()


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
