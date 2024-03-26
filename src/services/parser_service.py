import asyncio
from datetime import time, datetime
from itertools import count
from typing import TypeAlias
from urllib.error import URLError
from xml.sax import SAXException

import feedparser
from feedparser import FeedParserDict
from httpx import HTTPStatusError, AsyncClient, Response

from src.config.file_env import settings
from src.config.logger import Logger

FeedParserDict: TypeAlias = FeedParserDict[
    str, bool | URLError | tuple[str | None, bytes, dict] | int | SAXException
]
ListOfNewsData: TypeAlias = list[dict[str, str | list[dict] | dict | bool | time]]

logger = Logger.logger


class ParserNewsService:
    """Парсим новости."""
    client = AsyncClient

    @classmethod
    async def __get_response(cls, url: str) -> Response:
        """Получить ответ в виде xml-формата."""
        for attempt in count(start=1):
            try:
                response = await cls.client().get(url)
                response.raise_for_status()
                logger.info(
                    {
                        "event": f"{cls.__class__.__name__}",
                        "message": "Ответ 200 успешно создан.",
                        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M")
                    }
                )
                return response
            except HTTPStatusError as exc:
                if attempt == 3:
                    logger.error(
                        {
                            "event": f"{cls.__class__.__name__}",
                            "message": "Ошибка получения данных! "
                                       "Попытки его получения исчерпаны.",
                            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "error_info": exc,
                        }
                    )
                await asyncio.sleep(settings.time_sleep)
                continue

    @staticmethod
    def __get_feed_parser_dict(response: Response) -> FeedParserDict:
        """Получить из ответа xml-формата - словарь анализатора каналов."""
        return feedparser.parse(response.text)

    @staticmethod
    def __get_news_recordings(feed_parser_dict: FeedParserDict) -> ListOfNewsData:
        """Получить записи новостей (от старых к новым)."""
        return feed_parser_dict.entries[::-1]

    @classmethod
    async def execute_parser_news_and_get_entries(cls, url: str) -> ListOfNewsData:
        response = await cls.__get_response(url)
        feed_parser_dict = cls.__get_feed_parser_dict(response)
        entries = cls.__get_news_recordings(feed_parser_dict)
        return entries
