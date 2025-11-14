from typing import Any
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, JSON
from src.core.database import Base

class BookORM(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    author: Mapped[str | None] = mapped_column(String(255))
    year: Mapped[int | None]
    genre: Mapped[str | None] = mapped_column(String(100))
    count_page: Mapped[int] = mapped_column(default=0)
    accessibility: Mapped[str] = mapped_column(String(50), default="в наличии")
    external: Mapped[dict[str, Any] | None] = mapped_column(JSON)