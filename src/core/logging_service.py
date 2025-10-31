import sys
from pathlib import Path

from loguru import logger


class LoggerService:
    def __init__(self, name: str = "app", log_file: str = "app.log"):
        # Удаляем стандартные "handlers", чтобы не дублировались
        logger.remove()

        # Консольный вывод (цветной)
        logger.add(
            sys.stdout,
            colorize=True,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>",
            level="INFO",
        )

        # Лог-файл (с ротацией)
        log_path = Path(log_file)
        logger.add(
            log_path,
            rotation="10 MB",  # создаёт новый файл каждые 10MB
            retention="10 days",  # хранит 10 дней
            compression="zip",  # архивирует старые логи
            encoding="utf-8",
            level="INFO",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        )

        self._logger = logger.bind(context=name)

    def info(self, msg: str):
        self._logger.info(msg)

    def error(self, msg: str, exc: Exception | None = None):
        if exc:
            self._logger.exception(f"{msg}: {exc}")
        else:
            self._logger.error(msg)

    def warning(self, msg: str):
        self._logger.warning(msg)

    def debug(self, msg: str):
        self._logger.debug(msg)

    def get_logger(self):
        return self._logger


if __name__ == '__main__':

    logger = LoggerService("BookRepository")

    logger.info("Добавляем новую книгу")
    try:
        raise ValueError("Ошибка при вставке")
    except Exception as e:
        logger.error("Не удалось добавить книгу", e)
