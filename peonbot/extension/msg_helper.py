from typing import Dict
from aiogram.types import Message, ChatType

class MessageHelper:

    def __init__(self, message: Message):
        self.msg = message

    """
    Properties
    """
    @property
    def message_id(self):
        return str(self.msg.message_id)

    @property
    def chat(self):
        return self.msg.chat

    @property
    def chat_id(self):
        return str(self.chat.id)
    
    @property
    def user_id(self):
        return str(self.user.id)

    @property
    def reply_msg(self):
        return self.msg.reply_to_message

    @property
    def bot(self):
        return self.msg.bot

    @property
    def content_type(self):
        return str(self.msg.content_type)

    @property
    def content(self) -> any:
        return self.msg[self.msg.content_type]


    """
    Match Type
    """
    def is_from_super_group(self) -> bool:
        return self.chat.type == ChatType.SUPERGROUP

    def is_text(self) -> bool:
        return self.msg.content_type == "text"
