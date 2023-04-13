from peonbot.models.redis import BehaviorRecord
from peonbot.bussiness.repositories import RecordRepository


class RecordService:

    def __init__(self, record_repo: RecordRepository):
        self.record_repo = record_repo

    async def get_point(self, chat_id: str, user_id: str):
        return await self.record_repo.get_point(chat_id, user_id)

    async def set_cache_point(self, chat_id: str, user_id: str, point: int):
        data = BehaviorRecord(
            user_id=user_id,
            msg_count=point
        )

        await self.record_repo.set_cache(chat_id, data)

    async def set_db_point(self, chat_id: str, user_id: str, point: int):
        data = BehaviorRecord(
            user_id=user_id,
            msg_count=point
        )

        await self.record_repo.set_db(chat_id, data)
