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


@pytest.mark.skip(reason="This test sends a real SMS, use with caution")
def test_send_sms():
    response = send_sms("01012345678", "테스트 메시지", AuthType.VERIFICATION)
    assert response["status"] == "SUCCESS"
