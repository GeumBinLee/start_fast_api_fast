import json
from urllib.parse import urlencode

import requests


def get(url: str, params):
    return requests.get(url=url, params=params)


def post(url: str, params, body):
    query_string = urlencode(params)
    if query_string:
        query_string = "?" + query_string
    headers = {"Content-Type": "application/json", "charset": "UTF-8", "Accept": "*/*"}
    data = json.dumps(body, ensure_ascii=False, indent="\t")
    return requests.post(url=url + query_string, headers=headers, data=data)
