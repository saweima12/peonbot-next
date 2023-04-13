from peonbot.extensions.pydantic_ext import OrjsonBaseModel

class BehaviorRecord(OrjsonBaseModel):
    user_id: str
    full_name: str = ""
    msg_count: int = 0
