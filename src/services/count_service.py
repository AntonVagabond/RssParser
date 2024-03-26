import json
from collections import Counter
from datetime import datetime, timedelta
from typing import Generator, Any, TypeAlias

GeneratorNewsToday: TypeAlias = Generator[dict[str, str], Any, None]


class CountNewsService:
    """Подсчет количества новостей."""

    @staticmethod
    def __get_news() -> list[dict[str, str]]:
        """Получить файл для чтения."""
        with open(file="news.json", mode="r", encoding="utf-8") as file:
            file_content = file.read()
            news = json.loads(file_content)
            return news

    @staticmethod
    def __get_today() -> datetime:
        """Получить сегодняшнюю дату."""
        return datetime.now()

    @staticmethod
    def __get_yesterday(today: datetime) -> datetime:
        """Получить вчерашнюю дату."""
        return today - timedelta(days=1)

    @staticmethod
    def __get_news_today(
            news: list[dict[str, str]], yesterday: datetime,
    ) -> GeneratorNewsToday:
        """Получить сегодняшние новости."""
        news_today = (entry for entry in news
                      if datetime.fromisoformat(entry['date']) > yesterday)
        return news_today

    @staticmethod
    def __get_category_counter(news_today: GeneratorNewsToday) -> Counter[str]:
        """Получить подсчет категорий в новостях."""
        return Counter([item['category'] for item in news_today])

    @staticmethod
    def __get_most_common_category(category_counter: Counter[str]) -> str:
        """Получить наиболее распространенную категорию."""
        return category_counter.most_common(1)[0][0]

    @classmethod
    def execute_news_count(cls) -> None:
        """Выполнить подсчет новостей."""
        news = cls.__get_news()
        today = cls.__get_today()
        yesterday = cls.__get_yesterday(today)
        news_today = cls.__get_news_today(news, yesterday)
        category_counter = cls.__get_category_counter(news_today)
        popular_category = cls.__get_most_common_category(category_counter)
        print(f"Самая популярная категория - {popular_category}.")
        print('\n'.join(f"{pl} - {category}" for pl, category in
                        zip((1, 2, 3, 4), category_counter)))
