import pytest
from fastapi import Request

from app.core.exceptions import ReturnHandler


def test_return_handler():
    handler = ReturnHandler(message="Test message", status_code=400)
    assert handler.message == "Test message"
    assert handler.status_code == 400
