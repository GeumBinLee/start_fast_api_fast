from enum import Enum, auto


class StringEnum(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    @classmethod
    def values(cls):
        return [e.value for e in cls]


class AuthType(str, StringEnum):
    VERIFICATION = auto()
    PASSWORD = auto()
