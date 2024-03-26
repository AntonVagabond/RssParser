from src.config.file_env import settings
from src.services.count_service import CountNewsService
from src.services.parser_service import ParserNewsService
from src.services.record_service import RecordNewsService


class RssParser:
    """Класс где происходят все операции."""
    __parser_news = ParserNewsService
    __record_news = RecordNewsService
    __count_news = CountNewsService

    @classmethod
    async def execute_activities(cls) -> None:
        """Выполнить операции."""
        rss_link = settings.rss_link
        entries = (await cls.__parser_news
                   .execute_parser_news_and_get_entries(rss_link))
        cls.__record_news.execute_record(entries)
        cls.__count_news.execute_news_count()
