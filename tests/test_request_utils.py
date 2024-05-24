import pytest
from fastapi import Request

from app.core.request_utils import get_base_url


def test_get_base_url():
    class MockRequest:
        def __init__(self, base_url):
            self.base_url = base_url

    request = MockRequest(base_url="http://testserver")
    assert get_base_url(request) == "http://testserver"
    assert get_base_url(None) == "http://localhost:8000"
