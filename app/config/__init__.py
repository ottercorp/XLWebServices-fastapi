import os
import json
from pydantic import BaseSettings, RedisDsn


class Settings(BaseSettings):
    app_name: str = "XLWebServices-fastapi"
    root_path: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    file_cache_dir: str = "cache"
    repo_cache_dir: str = "repo"
    redis_host: str = 'localhost'
    hosted_url: str = 'https://aonyx.ffxiv.wang'
    redis_port: str = '6379'
    github_token: str = ''
    cache_clear_key: str = ''
    dalamud_repo: str = ''
    asset_repo: str = ''
    plugin_repo: str = ''
    plugin_api_level: int = 7
    xl_repo: str = ''

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        fields = {
            'app_name': {
                'env': 'app_name',
            },
            'file_cache_dir': {
                'env': 'file_cache_dir',
            },
            'repo_cache_dir': {
                'env': 'repo_cache_dir',
            },
            'github_token': {
                'env': 'github_token',
            },
            'cache_clear_key': {
                'env': 'cache_clear_key',
            },
            'redis_host': {
                'env': 'redis_host',
            },
            'redis_port': {
                'env': 'redis_port',
            },
            'hosted_url': {
                'env': 'hosted_url',
            },
            'plugin_api_level': {
                'env': 'plugin_api_level',
            }
        }

print("Loading settings as:")
print(json.dumps(Settings().dict(), indent=2))
