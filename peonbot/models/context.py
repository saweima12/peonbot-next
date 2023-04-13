from dataclasses import dataclass
from peonbot.models.redis import ChatConfig

@dataclass
class MessageContext:
    chat_config: ChatConfig
    is_admin: bool
    is_whitelist: bool
    point: int
    mark_delete: bool
    mark_record: bool
    msg: str = ""
