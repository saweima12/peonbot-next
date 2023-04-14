from peonbot.models.redis import UserRecord
from peonbot.bussiness.repositories import RecordRepository


class RecordService:

    def __init__(self, record_repo: RecordRepository):
        self.record_repo = record_repo

    async def get_record(self, chat_id: str, user_id: str) -> UserRecord:
        return await self.record_repo.get_user_record(chat_id, user_id)

    async def set_cache_point(self, chat_id: str, user_id: str, full_name: str, point: int):
        data = UserRecord(
            user_id=user_id,
            full_name=full_name,
            msg_count=point
        )

        await self.record_repo.set_cache(chat_id, data)

    async def set_db_point(self, chat_id: str, user_id: str, full_name: str, point: int):
        data = UserRecord(
            user_id=user_id,
            full_name=full_name,
            msg_count=point
        )

        await self.record_repo.set_db(chat_id, data)
