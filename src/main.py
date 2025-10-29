from fastapi import FastAPI

from src.api.books_router import router as books_router

app = FastAPI(title='Books API')
app.include_router(books_router)
