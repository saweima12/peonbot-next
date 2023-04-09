from aiogram import Bot
from aiogram.types import Message, ChatType

class MessageHelper:

    def __init__(self, message: Message):
        self.msg = message

    @property
    def bot(self) -> Bot:
        return self.msg.bot

    @property
    def content_type(self):
        return str(self.msg.content_type)

    @property
    def content(self) -> any:
        return self.msg[self.msg.content_type]

    @property
    def sender_id(self) -> str:
        return str(self.msg.from_user.id)

    @property
    def chat_id(self) -> str:
        return str(self.msg.chat.id)

    @property
    def chat_name(self) -> str:
        return str(self.msg.chat.full_name)

    def is_media(self) -> bool:
        return self.content_type in ["sticker", "animation"]

    def is_text(self) -> bool:
        return self.msg.content_type == "text"

    def is_sticker(self) -> bool:
        return self.msg.content_type == "sticker"

    def is_animation(self) -> bool:
        return self.msg.content_type == "animation"

    def is_supergroup(self) -> bool:
        return self.msg.chat.type == ChatType.SUPERGROUP