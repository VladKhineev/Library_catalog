import time

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.api.books_router import router as books_router
from src.core.logging_service import LoggerService

app = FastAPI(title='Books API')
app.include_router(books_router)

log_service = LoggerService()
logger = log_service.get_logger()
logger.info("App started")


# Middleware для логирования запросов
@app.middleware("http")
async def log_requests(request, call_next):
    start_time = time.time()
    logger.info(f"📥 {request.method} {request.url}")

    try:
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        logger.info(
            f"📤 {request.method} {request.url} -> {response.status_code} ({process_time:.2f} ms)"
        )
        return response
    except Exception as e:
        logger.exception(f"❌ Ошибка при обработке запроса: {e}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error"},
        )


#  Глобальный перехват исключений FastAPI
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.exception(f"🔥 Неперехваченное исключение: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Что-то пошло не так"},
    )


@app.get("/")
async def root():
    logger.info("Запрос корневого эндпоинта")
    return {"message": "Hello, Loguru!"}
