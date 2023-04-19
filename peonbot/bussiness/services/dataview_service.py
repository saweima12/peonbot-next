from typing import List
from datetime import datetime, timedelta, time

from peonbot.models.db import PeonChatConfig, PeonDeletedMessage, PeonBehaviorRecord
class DataViewService:

    async def get_avaliable_chats(self) -> List[PeonChatConfig]:
        result = await PeonChatConfig.filter(status="ok")
        return result
    
    async def get_chat_by_id(self, chat_id: str) -> PeonChatConfig | None:
        result = await PeonChatConfig.get_or_none(chat_id=chat_id)
        if result is None:
            return None
        return result


    async def get_deleted_context(self, chat_id: str) -> List[dict] | None:
        now = datetime.combine(datetime.utcnow(), time(15, 0))
        start_time = now - timedelta(days=1)
        data = await PeonDeletedMessage.filter(chat_id=chat_id, record_date__gte=start_time)

        if not data:
            return None

        result = dict()
        for item in data:
            user = item.message_json.get("from")
            # get user_id and full_name
            _key = user.get("id")

            first_name = user.get("first_name")
            last_name = user.get("last_name")

            _value = f"{first_name} {last_name}"
            # add to dictionary
            result[_key] = _value

        return {
            'count': len(data),
            'senders': list(result.items())
        }


    async def get_deleted_message(self, chat_id: str) -> List[PeonDeletedMessage] | None:
        # get search params
        start_time = (datetime.utcnow() - timedelta(days=14)).strftime("%Y-%m-%d")
        data = await PeonDeletedMessage.filter(chat_id=chat_id, record_date__gte=start_time)

        if not data:
            return None

        return data

    async def get_member_data(self, chat_id: str) -> List[dict] | None:

        data = await PeonBehaviorRecord.filter(chat_id=chat_id)

        if not data:
            return []

        return data

    def format_delete_msg(self, msg: dict) -> dict:
        _remove_field = ["chat", "sticker", "photo", "animation", "audio", "video", "voice", "from"]
        for _field in _remove_field:
            self.remove_field(_field, msg)
        return msg

    def get_full_name(self, msg: dict) -> str:
        user: dict = msg.get("from")
        first_name = user.get("first_name", "")
        last_name = user.get("last_name", "")
        return f"{first_name} {last_name}"

    def get_user_id(self, msg:dict) -> str:
        user: dict = msg.get("from")
        return str(user.get("id"))

    def get_username(self, msg:dict) -> str:
        user: dict= msg.get("from", "")
        return str(user.get("username", ""))

    def remove_field(self, key: str, obj: dict) -> dict:
        if key in obj:
            obj.pop(key)
        return obj
