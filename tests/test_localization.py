import json
from unittest.mock import mock_open, patch

import pytest

from app.core.localization import LANGUAGES, load_languages, translate

FILE_PATH = "resources/languages/"
DEFAULT_LANGUAGE = "en"


def test_load_languages(monkeypatch):
    """
    언어 파일을 로드하여 전역 변수에 저장합니다.
    """
    mock_en_data = json.dumps({"hello": "Hello", "goodbye": "Goodbye"})

    mock_ko_data = json.dumps({"hello": "안녕하세요", "goodbye": "안녕히 가세요"})

    mock_open_file = mock_open()
    mock_open_file.side_effect = [
        mock_open(read_data=mock_en_data).return_value,
        mock_open(read_data=mock_ko_data).return_value,
    ]

    monkeypatch.setattr("builtins.open", mock_open_file)

    load_languages()
    assert LANGUAGES["en"] == json.loads(mock_en_data)
    assert LANGUAGES["ko"] == json.loads(mock_ko_data)


def test_translate():
    """
    주어진 키에 대해 지정된 언어로 번역된 문자열을 반환합니다.
    """
    LANGUAGES["en"] = {"hello": "Hello", "goodbye": "Goodbye"}
    LANGUAGES["ko"] = {"hello": "안녕하세요", "goodbye": "안녕히 가세요"}

    assert translate("en", "hello") == "Hello"
    assert translate("ko", "hello") == "안녕하세요"
    assert translate("en", "nonexistent_key") == "nonexistent_key"
    assert translate("ko", "goodbye") == "안녕히 가세요"
