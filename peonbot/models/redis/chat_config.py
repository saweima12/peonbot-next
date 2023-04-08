from typing import List
from peonbot.extensions.pydantic_ext import OrjsonBaseModel

from peonbot.models.common import Status

class ChatConfig(OrjsonBaseModel):

    status: Status = Status.OK
    senior_count: int = 300
    check_lowest_count: int = 20
    adminstrators: List[str] = []
    allow_forward: List[str] = []
    block_name_keywords: List[str] = []
