import logging
import sys


class Logger:
    """Класс регистратора."""
    # Получить регистратор.
    logger = logging.getLogger()

    # Создать формат.
    formatter = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(message)s")

    # Создать обработчик.
    stream_handler = logging.StreamHandler(sys.stdout)
    file_handler = logging.FileHandler("app.log", encoding="utf-8")

    # Установить формат.
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Добавить обработчик для регистратора.
    logger.handlers = [stream_handler, file_handler]

    # Установить log-level.
    logger.setLevel(logging.INFO)
