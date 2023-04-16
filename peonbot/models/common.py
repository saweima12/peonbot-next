from enum import Enum

class Status(str, Enum):
    OK = 'ok'
    NG = 'ng'
    UNKNOWN = 'unknown'

class MemberLevel(int, Enum):
    NONE = 0
    JUNIOR = 1
    SENIOR = 2


class PermissionLevel(int, Enum):
    DENY = 0
    LIMIT = 1
    ALLOW = 2
