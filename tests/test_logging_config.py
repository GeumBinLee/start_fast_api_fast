import datetime
import logging
from unittest.mock import MagicMock, mock_open, patch

import pytest
from loguru import logger

from app.config.logging_config import InterceptHandler, Rotator


def test_rotator_should_rotate():
    rotator = Rotator(size=100, at=datetime.time(0, 0, 0))

    # 모의 객체 생성
    message = MagicMock()
    message.record = MagicMock()
    message.record["time"].timestamp.return_value = datetime.datetime.now().timestamp()

    # 파일 크기가 제한을 초과하지 않는 경우
    mock_file = MagicMock()
    mock_file.tell.return_value = 50  # 현재 파일 크기
    assert not rotator.should_rotate(message, mock_file)

    # 파일 크기가 제한을 초과하는 경우
    mock_file.tell.return_value = 101  # 현재 파일 크기
    assert rotator.should_rotate(message, mock_file)

    # 시간 제한을 초과하는 경우
    future_time = datetime.datetime.now() + datetime.timedelta(days=1)
    message.record["time"].timestamp.return_value = future_time.timestamp()
    assert rotator.should_rotate(message, mock_file)


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


@patch("app.config.logging_config.logger")
def test_intercept_handler_emit_with_attribute_error(mock_logger):
    handler = InterceptHandler()

    # Mock logger.level to raise AttributeError
    mock_logger.level.side_effect = AttributeError

    record = MagicMock()
    record.levelno = "INFO"
    record.exc_info = None

    handler.emit(record)

    mock_logger.opt.assert_called_once()
    mock_logger.opt().log.assert_called_once_with(record.levelno, record.getMessage())


@patch("app.config.logging_config.sys")
def test_intercept_handler_emit_with_frame(mock_sys):
    handler = InterceptHandler()

    mock_frame = MagicMock()
    mock_frame.f_code.co_filename = logging.__file__
    mock_sys._getframe.return_value = mock_frame

    record = MagicMock()
    record.levelname = "INFO"
    record.exc_info = None

    with patch.object(logger, "opt") as mock_opt:
        handler.emit(record)
        mock_opt.assert_called_once()
        mock_opt().log.assert_called_once_with("INFO", record.getMessage())
