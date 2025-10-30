import functools
from loguru import logger
from fastapi import HTTPException

import src.core.exceptions as exception

def handle_error(default_return=None, http_error: int | None = None, msg: str | None = None):
    """
       Универсальный декоратор для логирования ошибок.
       Можно использовать и в сервисах, и в эндпоинтах FastAPI.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except exception.BookNotFoundError as e:
                log = getattr(self, "logger", logger)
                log.warning(f"[404] {e}")
                raise HTTPException(status_code=404, detail=str(e))
            except AttributeError as e:
                log = getattr(self, "logger", logger)
                log.warning(f"[404] {e}")
                raise HTTPException(status_code=404, detail=str(e))
            except Exception as e:
                log = getattr(self, 'logger', logger)
                log.exception(f"Ошибка в {self.__class__.__name__}.{func.__name__}: {e}")
                if http_error:
                    raise HTTPException(status_code=http_error, detail=msg or str(e))
                return default_return

        return wrapper
    return decorator