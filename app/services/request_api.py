import json
from urllib.parse import urlencode

import requests


def get(url: str, params):
    return requests.get(url=url, params=params)


def post(url: str, params, body):
    """
    POST 요청을 보내고 응답을 반환합니다.
    :param url: 요청할 URL
    :param params: 요청 파라미터
    :param body: 요청 본문
    :return: 요청 응답 객체
    """
    query_string = urlencode(params)
    if query_string:
        query_string = "?" + query_string
    headers = {"Content-Type": "application/json", "charset": "UTF-8", "Accept": "*/*"}
    data = json.dumps(body, ensure_ascii=False, indent="\t")
    return requests.post(url=url + query_string, headers=headers, data=data)
