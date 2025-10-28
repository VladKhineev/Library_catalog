from fastapi import FastAPI

import src.models as models
from src.book_manager import BookManager

app = FastAPI()


@app.get('/get_books')
def get_books(repo: str):
    bm = BookManager(repo)
    return bm.get_books()

@app.get('/get_book/{book_id}')
def get_book(repo: str, book_id: int):
    bm = BookManager(repo)
    return bm.get_book(book_id)

@app.post('/')
def add_book(repo: str, book: models.Book):
    bm = BookManager(repo)
    return bm.add_book(book)

@app.put('/')
def update_book(repo: str, book_id: int, book: models.Book):
    bm = BookManager(repo)
    return bm.update_book(book_id, book)

@app.delete('/{book_id}')
def delete_book(repo: str, book_id: int):
    bm = BookManager(repo)
    return bm.delete_book(book_id)