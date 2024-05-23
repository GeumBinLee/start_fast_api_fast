import datetime
import logging
import os
import sys

from loguru import logger

JSON_LOGS = True if os.environ.get("JSON_LOGS", "0") == "1" else False


class Rotator:
    def __init__(self, *, size, at):
        now = datetime.datetime.now()
        self._size_limit = size
        self._time_limit = now.replace(hour=at.hour, minute=at.minute, second=at.second)

        if now >= self._time_limit:
            self._time_limit += datetime.timedelta(days=1)

    def should_rotate(self, message, file):
        file.seek(0, 2)
        if file.tell() + len(message) > self._size_limit:
            return True
        excess = message.record["time"].timestamp() - self._time_limit.timestamp()
        if excess >= 0:
            elapsed_days = datetime.timedelta(seconds=excess).days
            self._time_limit += datetime.timedelta(days=elapsed_days + 1)
            return True
        return False


class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )
