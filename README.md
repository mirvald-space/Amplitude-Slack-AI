# Data Analyzer Bot

Слак-бот для анализа CSV-файлов с использованием GPT-4o.

## Функциональность

- Анализ CSV-файлов при упоминании бота в сообщении с прикрепленным файлом
- Предоставление структурированного отчета на русском языке
- Кэширование результатов анализа для повторного использования
- Удаление сообщений бота из канала по команде "cleanup"

## Установка

1. Клонировать репозиторий:

```bash
git clone https://github.com/yourusername/data-analyzer-bot.git
cd data-analyzer-bot
```

2. Создать и активировать виртуальное окружение:

```bash
python -m venv venv
source venv/bin/activate  # Для Linux/Mac
# или
venv\Scripts\activate  # Для Windows
```

3. Установить зависимости:

```bash
pip install -r requirements.txt
```

4. Создать файл `.env` на основе `.env.example` и заполнить необходимые значения:

```bash
cp .env.example .env
```

## Настройка Slack

1. Создайте новое приложение Slack на [api.slack.com](https://api.slack.com/apps)
2. Добавьте следующие OAuth Scopes:
   - `app_mentions:read`
   - `chat:write`
   - `files:read`
   - `channels:history`
   - `chat:write.public`
3. Включите Socket Mode и Events API
4. Подпишитесь на событие `app_mentions`
5. Установите приложение в ваше рабочее пространство

## Запуск

```bash
python -m src.main
```

## Использование

1. Приглашение бота в канал:

```
/invite @data_analyzer_bot
```

2. Анализ CSV-файла - прикрепите файл и отметьте бота:

```
@data_analyzer_bot проанализируй этот файл
```

3. Удаление сообщений бота из канала:

```
@data_analyzer_bot cleanup
```

## Структура проекта

```
data_analyzer_bot/
├── requirements.txt
├── .env.example
├── README.md
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── clients/
│   │   ├── __init__.py
│   │   ├── slack_client.py
│   │   └── openai_client.py
│   ├── handlers/
│   │   ├── __init__.py
│   │   └── event_handlers.py
│   └── utils/
│       ├── __init__.py
│       └── formatters.py
└── tests/
    ├── __init__.py
    ├── test_slack_client.py
    ├── test_openai_client.py
    └── test_formatters.py
```
