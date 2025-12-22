import logging
from logging.handlers import RotatingFileHandler

from src.infrastructure.logger.interfaces import ILogger


class Logger(ILogger):
    def __init__(self):
        self.__logger = logging.getLogger()
        self.__logger.propagate = False
        self.__logger.setLevel(level=logging.INFO)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        file_handler = RotatingFileHandler(
            filename='logs/logs.log', mode='a', maxBytes=1048576, backupCount=5
        )
        file_handler.setFormatter(formatter)
        self.__logger.addHandler(file_handler)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.__logger.addHandler(console_handler)

        for name in ('uvicorn', 'uvicorn.error', 'uvicorn.access'):
            uv_logger = logging.getLogger(name)
            uv_logger.handlers = []
            uv_logger.propagate = False
            uv_logger.setLevel(logging.INFO)
            for handler in (file_handler, console_handler):
                uv_logger.addHandler(handler)

    def info(self, message):
        self.__logger.info(message)

    def error(self, message):
        self.__logger.error(message, exc_info=True)

    def warning(self, message):
        self.__logger.warning(message)

    def debug(self, message):
        self.__logger.debug(message)


logger = Logger()
