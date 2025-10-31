from abc import ABC, abstractmethod


class BaseApiClient(ABC):
    BASE_URL: str  # Каждый наследник должен задать свой базовый URL

    @abstractmethod
    async def fetch_book_info(self, *args, **kwargs):
        """Метод, который обязан реализовать каждый конкретный клиент"""
        pass
