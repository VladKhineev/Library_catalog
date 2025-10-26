from fastapi import FastAPI

import src.models as models
from src.bookManager import BookManager

app = FastAPI()

# get_books: получение списка всех книг с возможностью фильтрации
# get_book: получение информации о конкретной книге
# add_book: добавление новой книги в каталог
# update_book: обновление информации о книге
# delete_book: удаление книги из каталога

@app.get('/get_books')
def get_books():
    return '200'

@app.get('/get_book/{book_id}')
def get_book(book_id: int):
    return book_id

@app.post('/')
def add_book(book: models.Book):
    BookManager.add_book(book)
    return '200'

@app.patch('/')
def update_book(book: models.Book):
    return book

@app.delete('/{book_id}')
def delete_book(book_id: int):
    return book_id