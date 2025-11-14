from fastapi import Depends, Query
from loguru import logger
from src.core.config import Settings, get_settings
from src.core.database import AsyncSessionLocal
from src.integrations.base_api_client import BaseApiClient
from src.integrations.openlibrary_api import OpenLibraryAPI
from src.domain.managers.book_manager import BookManager
from src.domain.managers.enrichment_manager import BookEnrichmentManager
from src.api.schemas.repo import Repo
from src.data.repositories.base_repository import BaseBookRepository
from src.data.repositories.db_repository import DBBookRepository
from src.data.repositories.json_repository import JsonBookRepository
from src.data.repositories.jsonbin_repository import JsonBinRepository
from src.domain.services.book_service import BookService


def choose_repository(source: Repo) -> BaseBookRepository:
    settings: Settings = get_settings()
    if source == Repo.POSTGRES:
        repo = DBBookRepository(session_factory=AsyncSessionLocal, logger_instance=logger)
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


def get_source(source: Repo = Query(default=Repo.POSTGRES)) -> Repo:
    """Источник данных из query параметра"""
    return source

def get_repository(source: Repo = Depends(get_source)) -> BaseBookRepository:
    """Репозиторий на основе источника"""
    return choose_repository(source)

def get_book_manager(
    repo: BaseBookRepository = Depends(get_repository)
) -> BookManager:
    """Менеджер книг"""
    return BookManager(repo)

def get_openlibrary_api() -> OpenLibraryAPI:
    """API клиент OpenLibrary"""
    return OpenLibraryAPI()

def get_enrichment_manager(
    manager: BookManager = Depends(get_book_manager),
    api: OpenLibraryAPI = Depends(get_openlibrary_api)
) -> BookEnrichmentManager:
    """Менеджер с обогащением данных"""
    return BookEnrichmentManager(manager, api)

def get_book_service(
    enrichment_api: BaseApiClient = Depends(get_openlibrary_api),
    manager: BookManager = Depends(get_book_manager),
    enrichment_manager: BookEnrichmentManager = Depends(get_enrichment_manager),
) -> BookService:
    return BookService(enrichment_api, manager, enrichment_manager, logger)