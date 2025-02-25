import logging

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from config import LOG_LEVEL, SLACK_APP_TOKEN, SLACK_BOT_TOKEN
from handlers.event_handlers import register_handlers

logging.basicConfig(level=LOG_LEVEL)


def main():

    app = App(token=SLACK_BOT_TOKEN)

    register_handlers(app)

    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    print("Бот запущен и готов к работе!")
    handler.start()


if __name__ == "__main__":
    main()
