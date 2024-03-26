import json
from datetime import time, datetime
from typing import Optional, TypeAlias, Generator, Any, TextIO

from src.config.logger import Logger

ListOfNewsData: TypeAlias = list[dict[str, str | list[dict] | dict | bool | time]]

logger = Logger.logger


class RecordNewsService:
    """Запись новостей."""

    @classmethod
    def __get_news(cls, file: TextIO) -> list[Optional[dict[str, str]]]:
        """Получить список новостей либо пустой список."""
        try:
            news = json.load(file)
            logger.info(
                {
                    "event": f"{cls.__class__.__name__}",
                    "message": "Успешная загрузка записей из файла.",
                    "datetime": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
            )
            return news
        except json.decoder.JSONDecodeError:
            return []

    @staticmethod
    def __gen_entries(
            entries: ListOfNewsData,
    ) -> Generator[tuple[str, str, str], Any, None]:
        """Генератор записей."""
        for entry in entries:
            old_convert_time = datetime.strptime(
                entry["published"], "%a, %d %b %Y %H:%M:%S +%f"
            )
            new_convert_time = datetime.strftime(
                old_convert_time, "%Y-%m-%dT%H:%M:%S"
            )
            yield entry["title"], entry["category"], new_convert_time

    @staticmethod
    def __is_there_such_news(
            news_title: str, news: list[Optional[dict[str, str]]],
    ) -> bool:
        """Существуют ли уже такие новости."""
        return any(news_title == item.get('title') for item in news)

    @staticmethod
    def __append_news(
            news: list[Optional[dict[str, str]]],
            news_title: str,
            news_category: str,
            news_date: str,
    ) -> None:
        """Добавить новость в список новостей."""
        news.append(
            {"title": news_title, "category": news_category, "date": news_date}
        )

    @classmethod
    def __write_to_file(cls, news: list[dict[str, str]], file: TextIO) -> None:
        """Записать новости в файл."""
        json.dump(
            news, file, indent=4, ensure_ascii=False, separators=(',', ': ')
        )
        logger.info(
            {
                "event": f"{cls.__class__.__name__}",
                "message": "Успешная запись в файл.",
                "datetime": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
        )

    @classmethod
    def execute_record(cls, entries: ListOfNewsData) -> None:
        """Выполнить запись."""
        with open(file="news.json", mode="w+", encoding="utf-8") as file:
            file.seek(0)
            news = cls.__get_news(file)
            for news_title, news_category, news_date in cls.__gen_entries(entries):
                if cls.__is_there_such_news(news_title, news):
                    continue
                cls.__append_news(news, news_title, news_category, news_date)
            file.seek(0)
            cls.__write_to_file(news, file)
