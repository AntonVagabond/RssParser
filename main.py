import asyncio
from datetime import datetime

from src.config.file_env import settings
from src.start import RssParser


async def get_rss_parser() -> None:
    """Получить класс операций."""
    while True:
        one = datetime.now()
        await RssParser.execute_activities()
        await asyncio.sleep(settings.time_sleep)
        print(datetime.now() - one)

if __name__ == "__main__":
    asyncio.run(get_rss_parser())
