from fastapi import APIRouter, Depends

from src.Core import config

from src.managers.book_manager import BookManager
from src.models.book_model import Book
from src.models.repo_model import Repo

from src.repositories.db_repository import DBBookRepository
from src.repositories.json_repository import JsonBookRepository
from src.repositories.jsonbin_repository import JsonBinRepository

router = APIRouter(prefix='/books', tags=['Books'])

def get_book_manager(source: Repo):
    if source == Repo.POSTGRES:
        repo = DBBookRepository(dns=config.POSTGRES_URL)
    elif source == Repo.JSON:
        repo = JsonBookRepository()
    elif source == Repo.JSONBIN:
        repo = JsonBinRepository(master_key=config.MASTER_KEY, bin_id=config.BIN_ID)
    else:
        raise ValueError("Unknown source")
    return BookManager(repo)

@router.get('/')
def get_books(manager: BookManager = Depends(get_book_manager)):
    return manager.get_books()

@router.post('/')
def add_book(book: Book, manager: BookManager = Depends(get_book_manager)):
    return manager.add_book(book)


@router.get('/{book_id}')
def get_book(book_id: int, manager: BookManager = Depends(get_book_manager)):
    return manager.get_book(book_id)

@router.put('/')
def update_book(book: Book, manager: BookManager = Depends(get_book_manager)):
    return manager.update_book(book)

@router.delete('/{book_id}')
def delete_book(book_id: int, manager: BookManager = Depends(get_book_manager)):
    return manager.delete_book(book_id)