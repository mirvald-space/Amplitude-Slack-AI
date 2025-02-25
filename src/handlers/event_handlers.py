import hashlib
import logging

import requests
from slack_sdk.errors import SlackApiError

from clients.openai_client import analyze_with_gpt
from clients.slack_client import cleanup_bot_messages
from config import SLACK_BOT_TOKEN
from utils.formatters import convert_to_slack_markdown

# Cache for analysis results
analysis_cache = {}
logger = logging.getLogger(__name__)


def register_handlers(app):
    """
    Register all event handlers for the Slack app.

    Args:
        app: Slack app instance
    """

    @app.event("app_mention")
    def handle_mention(event, say):
        try:
            text = event.get("text", "").lower()
            channel = event["channel"]

            # Check for cleanup command
            if "cleanup" in text:
                cleanup_bot_messages(channel, say)
                return

            if "files" not in event:
                say("Пожалуйста, прикрепите CSV-файл к сообщению")
                return

            file_info = event["files"][0]
            if file_info.get("filetype") != "csv":
                say("Поддерживаются только CSV-файлы")
                return

            url = file_info["url_private"]
            headers = {"Authorization": f"Bearer {SLACK_BOT_TOKEN}"}
            with requests.get(url, headers=headers, stream=True) as response:
                response.raise_for_status()
                content = response.text

            content_hash = hashlib.sha256(content.encode()).hexdigest()
            if content_hash in analysis_cache:
                analysis = analysis_cache[content_hash]
                logger.info("Using cached analysis result")
            else:
                logger.info("Analyzing new content with GPT")
                analysis = analyze_with_gpt(content)
                analysis_cache[content_hash] = analysis

            slack_formatted_analysis = convert_to_slack_markdown(analysis)
            say(
                text=f"📊 *Результаты анализа:*\n{slack_formatted_analysis}",
                thread_ts=event["ts"],
            )

        except SlackApiError as e:
            logger.error(f"Slack API Error: {e.response['error']}")
            say("Ошибка взаимодействия с Slack")
        except requests.RequestException as e:
            logger.error(f"Request Error: {str(e)}")
            say("Ошибка загрузки файла")
        except Exception as e:
            logger.error(f"General Error: {str(e)}")
            say("Произошла внутренняя ошибка")
