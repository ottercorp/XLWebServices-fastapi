import redis
from .common import get_settings
from logs import logger

class Redis():
    @staticmethod
    def create_client():
        settings = get_settings()
        return redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0, decode_responses=True)


def load_plugin_count(plugin_count):
    settings = get_settings()
    r = Redis.create_client()
    total = 0
    for (plugin, count) in plugin_count.items():
        total += count
        r.hset(f'{settings.redis_prefix}plugin-count', plugin, count)
        logger.info(f'Setting plugin download counter of {plugin} to {count}')
    r.hset(f'{settings.redis_prefix}plugin-count', 'accumulated', total)


