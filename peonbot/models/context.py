from dataclasses import dataclass
from peonbot.models.common import MemberLevel
from peonbot.models.redis import ChatConfig, UserRecord

@dataclass
class MessageContext:
    chat_config: ChatConfig
    is_admin: bool
    is_whitelist: bool
    level: MemberLevel
    user_record: UserRecord
    mark_delete: bool
    mark_record: bool
    msg: str = ""
