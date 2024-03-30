import asyncio
from datetime import datetime

from src.config.file_env import settings
from src.services.count_service import CountNewsService
from src.services.parser_service import ParserNewsService
from src.services.record_service import RecordNewsService
from src.start import RssParser


async def get_rss_parser() -> None:
    """Получить класс операций."""
    while True:
        await RssParser(
            ParserNewsService, RecordNewsService, CountNewsService
        ).execute_activities(settings.rss_link)
        await asyncio.sleep(settings.time_sleep)

if __name__ == "__main__":
    asyncio.run(get_rss_parser())
