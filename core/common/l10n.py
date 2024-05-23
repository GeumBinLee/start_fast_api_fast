import json
from typing import Dict

FILE_PATH = "resources/languages/"
DEFAULT_LANGUAGE = "en"
LANGUAGES: Dict[str, Dict[str, str]] = {}


def load_languages():
    global LANGUAGES
    locales = ["en", "ko"]
    for locale in locales:
        try:
            with open(f"{FILE_PATH}{locale}.json", "r") as file:
                LANGUAGES[locale] = json.load(file)
        except FileNotFoundError:
            if locale == DEFAULT_LANGUAGE:
                raise RuntimeError(f"기본 언어 파일 [{DEFAULT_LANGUAGE}]을 찾을 수 없습니다.")
            # 기본 언어가 아니면 무시
            pass


def translate(locale: str, key: str) -> str:
    if key is None:
        return None

    languages = LANGUAGES.get(locale)
    if languages is None:
        languages = LANGUAGES.get(DEFAULT_LANGUAGE, {})
    
    lower_key = str(key).lower()
    return languages.get(lower_key, key)


# 프로그램 시작 시 언어 파일 로드
