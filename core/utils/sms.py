import datetime
import hashlib
import hmac
import platform
import random
import time
import uuid

import requests

from config.setting import get_settings
from core.common.enums import AuthType


def get_token():
    # between 0과 999999 사이의 랜덤한 정수 생성
    verification_code = random.randint(0, 999999)

    # 앞에 빈 곳에 0 채우기
    verification_code = str(verification_code).zfill(6)

    return verification_code


def unique_id():
    return str(uuid.uuid1().hex)


def get_iso_datetime():
    utc_offset_sec = time.altzone if time.localtime().tm_isdst else time.timezone
    utc_offset = datetime.timedelta(seconds=-utc_offset_sec)
    return (
        datetime.datetime.now()
        .replace(tzinfo=datetime.timezone(offset=utc_offset))
        .isoformat()
    )


def get_signature(key, msg):
    return hmac.new(key.encode(), msg.encode(), hashlib.sha256).hexdigest()


def get_headers(api_key, api_secret):
    date = get_iso_datetime()
    salt = unique_id()
    combined_string = date + salt

    return {
        "Authorization": "HMAC-SHA256 ApiKey="
        + api_key
        + ", Date="
        + date
        + ", salt="
        + salt
        + ", signature="
        + get_signature(api_secret, combined_string),
        "Content-Type": "application/json; charset=utf-8",
    }


def get_url(path):
    protocol = "https"
    domain = "api.coolsms.co.kr"
    prefix = ""
    url = "%s://%s" % (protocol, domain)
    if prefix != "":
        url = url + prefix
    url = url + path
    return url


def send_sms(phone_number: str, content: str, type: AuthType):
    settings = get_settings()
    api_key = settings.sms_api_key
    api_secret = settings.sms_api_secret
    sender = settings.sms_sender
    
    # TODO: 메세지 내용 바꾸기
    if type == AuthType.VERIFICATION:
        message = f"고객님의 인증번호는 [{content}]입니다. 감사합니다."
    if type == AuthType.PASSWORD:
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
