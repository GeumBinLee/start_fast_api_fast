import datetime
import hashlib
import hmac
import platform
import random
import time
import uuid

import requests

from app.config.settings import get_settings
from app.core.enums import AuthType


def get_token():
    """
    6자리 랜덤 인증번호를 생성하여 반환합니다.
    :return: 6자리 인증번호 문자열
    """
    verification_code = random.randint(0, 999999)
    return str(verification_code).zfill(6)


def unique_id():
    """
    고유한 ID를 생성하여 반환합니다.
    :return: 고유한 ID 문자열
    """
    return str(uuid.uuid1().hex)


def get_iso_datetime():
    """
    ISO 형식의 현재 날짜 및 시간을 반환합니다.
    :return: ISO 형식의 날짜 및 시간 문자열
    """
    utc_offset_sec = time.altzone if time.localtime().tm_isdst else time.timezone
    utc_offset = datetime.timedelta(seconds=-utc_offset_sec)
    return (
        datetime.datetime.now()
        .replace(tzinfo=datetime.timezone(offset=utc_offset))
        .isoformat()
    )


def get_signature(key, msg):
    """
    HMAC-SHA256 서명을 생성하여 반환합니다.
    :param key: 서명 키
    :param msg: 서명 메시지
    :return: 생성된 서명 문자열
    """
    return hmac.new(key.encode(), msg.encode(), hashlib.sha256).hexdigest()


def get_headers(api_key, api_secret):
    """
    CoolSMS API 요청을 위한 헤더를 생성하여 반환합니다.
    :param api_key: API 키
    :param api_secret: API 시크릿
    :return: 헤더 딕셔너리
    """
    date = get_iso_datetime()
    salt = unique_id()
    combined_string = date + salt
    return {
        "Authorization": f"HMAC-SHA256 ApiKey={api_key}, Date={date}, salt={salt}, signature={get_signature(api_secret, combined_string)}",
        "Content-Type": "application/json; charset=utf-8",
    }


def get_url(path):
    """
    CoolSMS API URL을 생성하여 반환합니다.
    :param path: API 경로
    :return: 생성된 URL 문자열
    """
    protocol = "https"
    domain = "api.coolsms.co.kr"
    url = f"{protocol}://{domain}{path}"
    return url


def send_sms(phone_number: str, content: str, type: AuthType):
    """
    SMS를 전송합니다.
    :param phone_number: 수신자 전화번호
    :param content: SMS 내용
    :param type: SMS 유형 (인증번호, 임시 비밀번호 등)
    :return: API 응답 JSON
    """
    settings = get_settings()
    api_key = settings.sms_api_key
    api_secret = settings.sms_api_secret
    sender = settings.sms_sender

    # 메시지 내용 설정
    if type == AuthType.VERIFICATION:
        message = f"고객님의 인증번호는 [{content}]입니다. 감사합니다."
    elif type == AuthType.PASSWORD:
        message = f"고객님의 임시 비밀번호는 [{content}]입니다. 감사합니다."

    data = {
        "agent": {
            "sdkVersion": "python/4.2.0",
            "osPlatform": platform.platform() + " | " + platform.python_version(),
        },
        "messages": [
            {
                "to": phone_number,
                "from": sender,
                "text": message,
            }
        ],
    }
    response = requests.post(
        get_url("/messages/v4/send-many"),
        headers=get_headers(api_key, api_secret),
        json=data,
    )
    return response.json()
