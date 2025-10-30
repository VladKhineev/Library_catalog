import functools
from curses import wrapper

from loguru import logger
from fastapi import HTTPException

def handle_error(default_return=None, http_error: int | None = None, msg: str | None = None):
    """
       Универсальный декоратор для логирования ошибок.
       Можно использовать и в сервисах, и в эндпоинтах FastAPI.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                log = getattr(self, 'logger', logger)
                log.exception(f"Ошибка в {self.__class__.__name__}.{func.__name__}: {e}")
                if http_error:
                    raise HTTPException(status_code=http_error, detail=msg or str(e))
                return default_return

        return wrapper
    return decorator