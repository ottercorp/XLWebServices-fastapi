import os
import json
from pydantic import BaseSettings
from typing import Dict, List

from logs import logger


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
    xivl_repo: str = ''
    dalamud_repo: str = ''
    distrib_repo: str = ''
    dalamud_format: str = 'zip'  # zip or 7z
    asset_repo: str = ''
    plugin_repo: str = ''
    plugin_api_level: int = 7
    plugin_api_level_test: int = 8
    api_namespace: Dict[int, str] = {
        7: 'plugin-PluginDistD17-main'
    }
    # CDN
    cdn_list: List[str] = []
    cf_token: str = ''
    cf_zone_id: str = ''
    ctcdn_ak: str = ''
    ctcdn_sk: str = ''
    # Crowdin
    crowdin_token: str = ''
    crowdin_project_name: str = 'Dalamud Plugins'
    default_pm_lang: str = 'en-US'  # Locale
    # Google Analytics
    ga_api_secret: str = ''
    # Plogon
    plogon_api_key: str = ''

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


SENSITIVE_FIELDS = [
    'github_token',
    'cache_clear_key',
    'cf_token',
    'ctcdn_ak',
    'ctcdn_sk',
    'crowdin_token',
    'api_secret',
    'plogon_api_key',
]
settings_json = Settings().dict()
for field in SENSITIVE_FIELDS:
    if field in settings_json:
        settings_json[field] = '*' * len(settings_json[field])

if 'is_show_settings' not in globals().keys():  # Preventing duplicate displays of settings
    logger.info("Loading settings as:")
    logger.info(json.dumps(settings_json, indent=2))
    is_show_settings = True
