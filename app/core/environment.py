from enum import auto

from app.core.enums import Currency, StringEnum


class Environment(str, StringEnum):
    LANGUAGE = (auto(), "언어", str, "korean")

    def __new__(cls, value, description, data_type, default_value):
        obj = str.__new__(cls, [value])
        obj._value_ = value
        obj.description = description
        obj.data_type = data_type
        obj.default_value = default_value
        return obj
