from typing import Dict
from aiogram.types import Message, Sticker, Animation, Video, VideoNote, Audio

class MessageHelper:

    def __init__(self, message: Message):
        self.msg = message

    @property
    def content_type(self):
        return str(self.msg.content_type)

    @property
    def content(self) -> any:
        return self.msg[self.msg.content_type]

    @property
    def user_id(self) -> str:
        return str(self.msg.from_user.id)

    def is_media(self) -> bool:
        return self.content_type in ["sticker", "animation"]

    def is_text(self) -> bool:
        return self.msg.content_type == "text"
    
    def is_sticker(self) -> bool:
        return self.msg.content_type == "sticker"
    
    def is_animation(self) -> bool:
        return self.msg.content_type == "animation"
    