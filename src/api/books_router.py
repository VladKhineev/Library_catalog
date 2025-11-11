from fastapi import APIRouter, Depends, status, Query
from src.core.decorators import handle_error
from src.dependencies.dependencies import get_book_service
from src.models.book_model import Book, BookCreateDTO, BookResponseDTO, BookUpdateDTO
from src.services.book_service import BookService

router = APIRouter(prefix='/api/v1/books', tags=['Books'])


@handle_error(default_return=[], msg='Error getting a list of books')
@router.get('/', response_model=list[Book], status_code=status.HTTP_200_OK)
async def get_books(
        offset: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100),
        service: BookService = Depends(get_book_service)) -> list[BookResponseDTO]:
    return await service.get_list_books(offset=offset, limit=limit)


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
