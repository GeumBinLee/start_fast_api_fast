from unittest.mock import patch

import pytest

from app.core.enums import AuthType
from app.services.sms_service import get_token, send_sms, unique_id


def test_get_token():
    token = get_token()
    assert len(token) == 6
    assert token.isdigit()


def test_unique_id():
    uid = unique_id()
    assert len(uid) > 0


def mock_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code
            self.text = str(json_data)  # 응답 내용을 문자열로 설정

        def json(self):
            return self.json_data

    # 원하는 모의 응답 데이터 설정
    if args[0] == "https://api.coolsms.co.kr/messages/v4/send-many":
        return MockResponse({"status": "SENDING"}, 200)

    return MockResponse(None, 404)


@patch("requests.post", side_effect=mock_requests_post)
def test_send_sms(mock_post):
    response = send_sms("01043996646", "테스트 메시지", AuthType.VERIFICATION)
    assert response["status"] == "SENDING"
