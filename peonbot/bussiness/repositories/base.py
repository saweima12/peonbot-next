from peonbot.common.redis import RedisProxyFactory

class BaseRepository:

    def __init__(self, redis_factory: RedisProxyFactory):
        self.__redis_factory = redis_factory

    def redis_conn(self):
        return self.__redis_factory.get_connection()

    @property
    def factory(self):
        return self.__redis_factory