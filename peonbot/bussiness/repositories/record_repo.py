from typing import Dict
from peonbot.models.db import PeonBehaviorRecord
from peonbot.models.redis import UserRecord

from .base import BaseRepository


class RecordRepository(BaseRepository):

    async def get_record_cache(self, chat_id: str) -> Dict[str, UserRecord]:
        namespace = self.get_namespace(chat_id)

        async with self.redis_conn() as conn:
            proxy = self.factory.get_hash_map(namespace, conn)
            result: dict = await proxy.getall()

            if not result:
                return dict()

            for user_id, v in result.items():
                result[user_id] = UserRecord.parse_raw(v)

            return result


    async def get_user_record(self, chat_id: str, user_id: str) -> UserRecord:
        namespace = self.get_namespace(chat_id)

        # get record from cache.
        async with self.redis_conn() as conn:
            proxy = self.factory.get_hash_map(namespace, conn)
            result: str = await proxy.get(user_id)
            if result is not None:
                model = UserRecord.parse_raw(result)
                return model

        # not found in cache. try load from database.
        record = await PeonBehaviorRecord.get_or_none(chat_id=chat_id, user_id=user_id)
        if record:
            record = UserRecord(
                chat_id=record.chat_id,
                user_id=record.user_id,
                full_name=record.full_name,
                msg_count=record.msg_count,
                created_time=record.created_time
            )

            await self.set_cache(chat_id, record)
            return record

        return UserRecord(
            chat_id=chat_id,
            user_id=user_id
        )

    async def set_cache(self, chat_id: str, data: UserRecord):
        namespace = self.get_namespace(chat_id)

        async with self.redis_conn() as conn:
            proxy = self.factory.get_hash_map(namespace, conn)
            await proxy.set_key(data.user_id, data.json())

    async def clean_cache(self, chat_id: str):
        namespace = self.get_namespace(chat_id)

        async with self.redis_conn() as conn:
            proxy = self.factory.get_hash_map(namespace, conn)
            await proxy.delete()

    async def set_db(self, chat_id: str, data: UserRecord):

        await PeonBehaviorRecord.update_or_create(dict(
            full_name=data.full_name,
            msg_count=data.msg_count
        ), chat_id=chat_id, user_id=data.user_id)


    def get_namespace(self, chat_id):
        return f"{chat_id}:record"
