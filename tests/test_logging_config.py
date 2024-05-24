import datetime
import logging
from unittest.mock import MagicMock

import pytest
from loguru import logger

from app.config.logging_config import InterceptHandler, Rotator


def test_rotator_should_rotate():
    rotator = Rotator(size=100, at=datetime.time(0, 0, 0))

    # 모의 객체 생성
    message = MagicMock()
    message.record = MagicMock()
    message.record["time"].timestamp.return_value = datetime.datetime.now().timestamp()

    # /dev/null 대신 실제 파일 객체를 모의로 대체
    with open("/dev/null", "a") as file:
        assert not rotator.should_rotate(message, file)


def test_intercept_handler(caplog):
    handler = InterceptHandler()

    # Loguru 핸들러 추가
    logger.add(handler.emit, format="{message}", level="INFO")

    with caplog.at_level("INFO"):
        # 로그 메시지 생성
        logging.getLogger().info("Test log")

    # 로그 메시지 검증
    assert any("Test log" in message.message for message in caplog.records)

    # 핸들러 제거
    logger.remove()
