import logging

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from config import SLACK_BOT_TOKEN

slack_client = WebClient(SLACK_BOT_TOKEN)
logger = logging.getLogger(__name__)


def cleanup_bot_messages(channel: str, say):

    try:

        bot_info = slack_client.auth_test()
        bot_id = bot_info["bot_id"]

        response = slack_client.conversations_history(channel=channel, limit=100)
        messages = response["messages"]

        deleted_count = 0
        for message in messages:
            if message.get("bot_id") == bot_id:
                slack_client.chat_delete(channel=channel, ts=message["ts"])
                deleted_count += 1

        while response["has_more"]:
            response = slack_client.conversations_history(
                channel=channel,
                limit=100,
                cursor=response["response_metadata"]["next_cursor"],
            )
            messages = response["messages"]
            for message in messages:
                if message.get("bot_id") == bot_id:
                    slack_client.chat_delete(channel=channel, ts=message["ts"])
                    deleted_count += 1

        say(f"Удалено {deleted_count} сообщений от бота в этом канале.")

    except SlackApiError as e:
        logger.error(f"Slack API Error during cleanup: {e.response['error']}")
        say("Ошибка при очистке сообщений. Проверьте права бота или повторите позже.")
    except Exception as e:
        logger.error(f"General Error during cleanup: {str(e)}")
        say("Произошла внутренняя ошибка при очистке.")
