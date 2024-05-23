import json

FILE_PATH = "resources/languages/"
DEFAULT_LANGUAGE = "en"


def translate(locale: str, key: str):
    if key is None:
        return None

    try:
        with open(f"{FILE_PATH}{locale}.json", "r") as file:
            languages = json.load(file)
    except:
        try:
            locale = DEFAULT_LANGUAGE
            with open(f"{FILE_PATH}{locale}.json", "r") as file:
                languages = json.load(file)
        except:
            return key

    lower_key = str(key).lower()
    if lower_key not in languages:
        return key
    return languages[lower_key]
