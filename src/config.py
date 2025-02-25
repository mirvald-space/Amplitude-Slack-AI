import os

from dotenv import load_dotenv

load_dotenv()


LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()


SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]


OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

SYSTEM_PROMPT = """
Ты - опытный аналитик данных. Проанализируй CSV-файл и предоставь:
1. Ключевые метрики
2. Выявленные аномалии
3. Практические рекомендации
Формат: структурированный отчет на русском языке.
"""
