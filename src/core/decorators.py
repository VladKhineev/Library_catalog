import functools

from fastapi import HTTPException
from loguru import logger

import src.core.exceptions as exception


def handle_error(
    default_return=None, msg: str | None = None
):
    """
    Универсальный декоратор для логирования ошибок.
    Можно использовать и в сервисах, и в эндпоинтах FastAPI.
    """

    def decorator(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except exception.BookNotFoundError as e:
                raise HTTPException(status_code=404, detail=str(e))
            except Exception as e:
                logger.exception(f"Error in {func.__name__}: {e}")
                if msg:
                    raise HTTPException(status_code=500, detail=msg)
                return default_return

        return async_wrapper

    return decorator
