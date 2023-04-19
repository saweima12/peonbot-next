from typing import Any, Dict, List
from peonbot.extension.pydantic import OrjsonBaseModel

class ChatConfigModel(OrjsonBaseModel):
    senior_count: int = 300
    adminstrators: List[str] = []
    allow_forward: List[str] = []
    
