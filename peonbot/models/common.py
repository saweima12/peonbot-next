from enum import Enum

class Status(str, Enum):
    OK = 'ok'
    NG = 'ng'
    UNKNOWN = 'unknown'