import logging

class LoggerService:
    def __init__(self, name: str = 'app'):
        self.logger = logging.getLogger(name)
        if not self.logger.handlers:
            handler = logging.FileHandler('app.log', encoding='utf-8')
            formater = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            handler.setFormatter(formater)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def info(self, msg: str):
        self.logger.info(msg)

    def error(self, msg: str, exc: Exception | None = None):
        if exc:
            self.logger.exception(f'{msg}: {exc}')
        else:
            self.logger.error(msg)