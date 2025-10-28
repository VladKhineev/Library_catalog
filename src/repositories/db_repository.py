import psycopg2
from psycopg2.extras import RealDictCursor, RealDictRow

import src.models as models



class DBBookRepository:
    def __init__(self, dns: str):
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
            accessibility VARCHAR(50) DEFAULT 'в наличии'
        );
        '''
        with self._get_connection() as conn, conn.cursor() as cur:
            cur.execute(query)
            conn.commit()

    def add_book(self, book: models.Book) -> int:
        query = """
                INSERT INTO books (title, author, year, genre, count_page, accessibility)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id;
                """
        with self._get_connection() as conn, conn.cursor() as cur:
            cur.execute(query, (
                book.title,
                book.autor,
                book.year,
                book.genre,
                book.count_page,
                book.accessibility
            ))
            book_id = cur.fetchone()[0]
            conn.commit()
            return book_id

    def get_book(self, book_id: int) -> RealDictRow:
        query = "SELECT * FROM books WHERE id = %s;"
        with self._get_connection() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (book_id,))
            return cur.fetchone()

    def get_books(self) -> list:
        query = "SELECT * FROM books ORDER BY id;"
        with self._get_connection() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            return cur.fetchall()

    def update_book(self, book: models.Book) -> RealDictRow:
        query = """
                UPDATE books
                SET title = %s,
                    author = %s,
                    year = %s,
                    genre = %s,
                    count_page = %s,
                    accessibility = %s
                WHERE id = %s;
                """
        with self._get_connection() as conn, conn.cursor() as cur:
            cur.execute(query, (
                book.title,
                book.autor,
                book.year,
                book.genre,
                book.count_page,
                book.accessibility,
                book.id
            ))
            conn.commit()

        return self.get_book(book_id=book.id)

    def delete_book(self, book_id: int) -> list:
        query = "DELETE FROM books WHERE id = %s;"
        with self._get_connection() as conn, conn.cursor() as cur:
            cur.execute(query, (book_id,))
            conn.commit()

        return self.get_books()


if __name__ == '__main__':
    repo = DBBookRepository('postgresql://postgres:postgres@localhost:5432/Library')
    repo.create_table()

    book = models.Book(**{
        "id": 3,
        "title": "Dima",
        "autor": "string",
        "year": 100,
        "genre": "string",
        "count_page": 100,
        "accessibility": "в наличии"
    })


    print(repo.get_books())
    print(repo.get_book(2))
    print(repo.add_book(book))