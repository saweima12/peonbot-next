from typing import List
from datetime import datetime, timedelta

from peonbot.models.db import PeonChatConfig, PeonDeletedMessage, PeonBehaviorRecord
class DataViewService:

    async def get_chats(self) -> List[dict]:
        result = await PeonChatConfig.filter(status="ok")
        data = [{
            'chat_id': item.chat_id,
            'chat_name': item.chat_name,
            'config_json': item.config_json
        } for item in result]
        return data
    
    async def get_deleted_message(self, chat_id: str) -> List[dict] | None:
        # get search params
        start_time = (datetime.utcnow() - timedelta(days=14)).strftime("%Y-%m-%d")
        data = await PeonDeletedMessage.filter(chat_id=chat_id, record_date__gte=start_time)

        if not data:
            return None

        result = []
        for item in data:
            raw = self.format_delete_msg(item.message_json)
            result.append({
                'content_type': item.content_type,
                'raw': raw,
                'record_time': item.record_date.isoformat()
            })

        return result

    async def get_member_data(self, chat_id: str) -> List[dict] | None:

        data = await PeonBehaviorRecord.filter(chat_id=chat_id)

        if not data:
            return []

        result = [ {
            "user_id": item.user_id,
            "full_name": item.full_name,
            "point": item.msg_count,
            "last_updated": item.update_time.isoformat()
        } for item in data]

        return result

    def format_delete_msg(self, msg: dict) -> dict:
        _remove_field = ["chat", "sticker", "photo", "animation", "audio", "video", "voice", "from"]
        for _field in _remove_field:
            self.remove_field(_field, msg)
        return msg

    def remove_field(self, key: str, obj: dict) -> dict:
        if key in obj:
            obj.pop(key)
        return obj
