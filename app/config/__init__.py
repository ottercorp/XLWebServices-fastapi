import os
import json
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "XLWebServices-fastapi"
    root_path: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    file_cache_dir: str = "cache"
    repo_cache_dir: str = "repo"
    redis_host: str = 'localhost'
    redis_port: str = '6379'
    redis_prefix: str = 'xlweb-fastapi|'
    hosted_url: str = 'https://aonyx.ffxiv.wang'
    github_token: str = ''
    cache_clear_key: str = ''
    dalamud_repo: str = ''
    distrib_repo: str = ''
    dalamud_format: str = 'zip'
    asset_repo: str = ''
    plugin_repo: str = ''
    plugin_api_level: str = "7"
    xivl_repo: str = ''

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

print("Loading settings as:")
print(json.dumps(Settings().dict(), indent=2))
