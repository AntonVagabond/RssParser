# 📔 RssParser - Парсер новостной ленты.

## 📚 Основные зависимости.
```
Python 3.11
feedparser==6.0.11
httpx==0.27.0
pydantic==2.6.4
pydantic-settings==2.0.3
pydantic_core==2.16.3
python-dotenv==1.0.1
```
## 🔌 Установка.
1. Клонирование репозитория:
```git clone https://github.com/AntonVagabond/RssParser```
2. Создание виртуального окружения и установка зависимостей:
```
python3.8 -m venv env
source env/bin/activate
pip install -r requirements.txt
```
3. Заполнить файл .env.example и переименовать его .env.
4. Запуск бота. python bot.py

## 🔧 Особенности проекта.
1. Проект отслеживает и отображает удачные/неудачные получения записей и их загрузку  
в файл путем логирования и отображения на консоль и в файл app.log.
2. В проекте была частично реализована асинхронность.