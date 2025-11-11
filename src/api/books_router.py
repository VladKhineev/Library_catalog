from fastapi import APIRouter, Depends, status
from loguru import logger

from src.core.config import Settings, get_settings
from src.core.decorators import handle_error
from src.dependencies.dependencies import get_book_service
from src.integrations.openlibrary_api import OpenLibraryAPI
from src.managers.book_manager import BookManager
from src.managers.enrichment_manager import BookEnrichmentManager
from src.models.book_model import Book, BookCreateDTO, BookResponseDTO, BookUpdateDTO
from src.models.repo_model import Repo
from src.repositories.base_repository import BaseBookRepository
from src.repositories.db_repository import DBBookRepository
from src.repositories.json_repository import JsonBookRepository
from src.repositories.jsonbin_repository import JsonBinRepository
from src.services.book_service import BookService

router = APIRouter(prefix='/api/v1/books', tags=['Books'])


@handle_error(default_return=[], msg='Error getting a list of books')
@router.get('/', response_model=list[Book], status_code=status.HTTP_200_OK)
async def get_books(service: BookService = Depends(get_book_service)) -> list[BookResponseDTO]:
    return await service.get_list_books()


@handle_error(default_return=[], msg='Error when adding a workbook')
@router.post('/', response_model=BookResponseDTO, status_code=status.HTTP_201_CREATED)
async def add_book(
    book: BookCreateDTO, service: BookService = Depends(get_book_service)
) -> BookResponseDTO:
    return await service.create_book(book)


@handle_error(default_return=[], msg='Error receiving the book')
@router.get('/{book_id}', response_model=Book, status_code=status.HTTP_200_OK)
async def get_book(
    book_id: int, service: BookService = Depends(get_book_service)
) -> BookResponseDTO:
    return await service.get_book(book_id)


@handle_error(default_return=[], msg='Error when updating a workbook')
@router.put('/', response_model=Book, status_code=status.HTTP_200_OK)
async def update_book(
    book: BookUpdateDTO, service: BookService = Depends(get_book_service)
) -> BookResponseDTO:
    return await service.update_book(book)


@handle_error(default_return=[], msg='Error when deleting a book')
@router.delete('/{book_id}', response_model=Book, status_code=status.HTTP_200_OK)
async def delete_book(
    book_id: int, service: BookService = Depends(get_book_service)
) -> BookResponseDTO:
    return await service.delete_book(book_id)


@handle_error(default_return=[], msg='(Enriched): Error when adding a workbook')
@router.post('/enriched/', response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book_enriched(
    book: BookCreateDTO, service: BookService = Depends(get_book_service)
) -> BookResponseDTO:
    return await service.add_with_api(book)
