from datetime import datetime
from peonbot.models.common import MemberLevel
from peonbot.extensions.pydantic_ext import OrjsonBaseModel

class UserRecord(OrjsonBaseModel):
    user_id: str
    full_name: str = ""
    member_level: MemberLevel = MemberLevel.NONE
    msg_count: int = 0
    created_time: datetime = datetime.utcnow()
