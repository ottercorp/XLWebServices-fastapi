import redis
from .common import get_settings

class Redis():
    @staticmethod
    def create_client():
        settings = get_settings()
        return redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0, decode_responses=True)