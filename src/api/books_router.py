from fastapi import APIRouter, Depends
from loguru import logger

from src.core.config import Settings, get_settings
from src.core.decorators import handle_error
from src.integrations.openlibrary_api import OpenLibraryAPI
from src.managers.book_manager import BookManager
from src.managers.enrichment_manager import BookEnrichmentManager
from src.models.book_model import Book
from src.models.repo_model import Repo
from src.repositories.db_repository import DBBookRepository
from src.repositories.json_repository import JsonBookRepository
from src.repositories.jsonbin_repository import JsonBinRepository

router = APIRouter(prefix='/books', tags=['Books'])


def choose_repository(source: Repo):
    settings: Settings = get_settings()
    if source == Repo.POSTGRES:
        repo = DBBookRepository(dsn=settings.POSTGRES_URL, logger_instance=logger)
    elif source == Repo.JSON:
        repo = JsonBookRepository(logger)
    elif source == Repo.JSONBIN:
        repo = JsonBinRepository(
            master_key=settings.JSONBIN_MASTER_KEY,
            bin_id=settings.JSONBIN_BIN_ID,
            logger_instance=logger,
        )
    else:
        raise ValueError("Unknown source")
    return repo


def get_book_manager(source: Repo):
    repo = choose_repository(source)
    return BookManager(repo, logger)


def get_enrichment_manager(source: Repo) -> BookEnrichmentManager:
    manager = get_book_manager(source)
    api = OpenLibraryAPI()
    return BookEnrichmentManager(manager, api)


@handle_error(default_return=[], msg='Ошибка при получении списка книг')
@router.get('/')
async def get_books(manager: BookManager = Depends(get_book_manager)):
    return await manager.get_books()


@handle_error(default_return=[], msg='Ошибка при добавлении книги')
@router.post('/')
async def add_book(book: Book, manager: BookManager = Depends(get_book_manager)):
    return await manager.add_book(book)


@handle_error(default_return=[], msg='Ошибка при получении книги')
@router.get('/{book_id}')
async def get_book(book_id: int, manager: BookManager = Depends(get_book_manager)):
    return await manager.get_book(book_id)


@handle_error(default_return=[], msg='Ошибка при обновлении книги')
@router.put('/')
async def update_book(book: Book, manager: BookManager = Depends(get_book_manager)):
    return await manager.update_book(book)


@handle_error(default_return=[], msg='Ошибка при удалении книги')
@router.delete('/{book_id}')
async def delete_book(book_id: int, manager: BookManager = Depends(get_book_manager)):
    return await manager.delete_book(book_id)


@handle_error(default_return=[], msg='Ошибка при добавлении книги')
@router.post('/enriched/')
async def create_book_enriched(
    book: Book, manager: BookEnrichmentManager = Depends(get_enrichment_manager)
):
    return await manager.add_with_api(book)
