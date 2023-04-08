from typing import Set
from .base import BaseRepository


class BotConfigRepository(BaseRepository):

    def get_whitelist(self) -> Set[str]:
        namespace = self.get_namespace("config")

    
    def set_whitelist(self):
        pass


    def get_namespace(self, key: str) -> str:
        return f"bot:{key}"
