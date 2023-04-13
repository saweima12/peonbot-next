from peonbot.models.db import PeonBehaviorRecord
from peonbot.models.redis import BehaviorRecord

from .base import BaseRepository


class RecordRepository(BaseRepository):

    async def get_point(self, chat_id: str, user_id: str) -> int:
        namespace = self.get_namespace(chat_id)

        async with self.redis_conn() as conn:
            proxy = self.factory.get_hash_map(namespace, conn)
            result = await proxy.get(user_id)
            if result is not None:
                return int(result)
        return 0

    async def set_cache(self, chat_id: str, data: BehaviorRecord):
        namespace = self.get_namespace(chat_id)

        async with self.redis_conn() as conn:
            proxy = self.factory.get_hash_map(namespace, conn)
            await proxy.set_key(data.user_id, data.msg_count)

    async def set_db(self, chat_id: str, data: BehaviorRecord):

        await PeonBehaviorRecord.update_or_create(dict(
            msg_count=data.msg_count
        ), chat_id=chat_id, user_id=data.user_id)


    def get_namespace(self, chat_id):
        return f"{chat_id}:record"
