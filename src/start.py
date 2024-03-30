class RssParser:
    """Класс где происходят все операции."""

    __slots__ = ('__parser_news', '__record_news', '__count_news')

    def __init__(self, parser_news, record_news, count_news) -> None:
        self.__parser_news = parser_news
        self.__record_news = record_news
        self.__count_news = count_news

    async def execute_activities(self, rss_link: str) -> None:
        """Выполнить операции."""
        entries = (await self.__parser_news
                   .execute_parser_news_and_get_entries(rss_link))
        self.__record_news.execute_record(entries)
        self.__count_news.execute_news_count()
