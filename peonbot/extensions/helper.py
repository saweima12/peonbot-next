from typing import List
from aiogram import Bot
from aiogram.types import Message, ChatType, MessageEntity

from peonbot.utils.text_util import check_has_url
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
    def sender_fullname(self) -> str:
        return str(self.msg.from_user.full_name)

    @property
    def message_id(self) -> str:
        return str(self.msg.message_id)

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
    
    def is_forward(self) -> bool:
        return self.msg.is_forward()

    def get_custom_emoji(self) -> List[MessageEntity]:
        if self.msg.entities:
            emoji_entities = [entity for entity in self.msg.entities if entity.type == "custom_emoji"]
            if len(emoji_entities) > 0:
                return emoji_entities
        return None

    def get_mentions(self) -> List[MessageEntity]:
        if self.msg.entities:
            mention_entities = [entity for entity in self.msg.entities if entity.type == "mention"]
            if len(mention_entities) > 0:
                return mention_entities
        return None

    def has_url(self) -> bool:
        if self.msg.entities:
            url_entites = [entity for entity in self.msg.entities if entity.type == "url"]
            if len(url_entites) > 0:
                return True

        if self.is_text():
            return check_has_url(self.msg.text)
        return False
