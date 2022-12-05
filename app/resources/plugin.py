import os, sys
import re
import json
import codecs
from functools import cache
from app.config import Settings
from app.utils.common import get_settings, get_apilevel_namespace_map
from app.utils.responses import PrettyJSONResponse
from app.utils.redis import Redis
from app.utils.tasks import regen
from fastapi import APIRouter, HTTPException, Depends, Query, BackgroundTasks
from fastapi.responses import RedirectResponse

router = APIRouter()

@router.get("/Download/{plugin}")
async def plugin_download(plugin: str, isUpdate: bool = False, isTesting: bool = False, branch: str = '', settings: Settings = Depends(get_settings)):
    r = Redis.create_client()
    api_level = re.search(r'api(?P<level>\d+)', branch).group('level')
    if not api_level:
        api_level = settings.plugin_api_level
    else:
        api_level = int(api_level)
    apilevel_namespace_map = get_apilevel_namespace_map()
    if api_level not in apilevel_namespace_map:
        return HTTPException(status_code=400, detail="API level not supported")
    plugin_namespace = apilevel_namespace_map[api_level]
    plugin_name = plugin + '-testing' if isTesting else plugin
    plugin_hashed_name = r.hget(f'{settings.redis_prefix}{plugin_namespace}', plugin_name)
    if not plugin_hashed_name and isTesting:  # use stable if testing not exists
        plugin_hashed_name = r.hget(f'{settings.redis_prefix}{plugin_namespace}', plugin)
    if not plugin_hashed_name:
        raise HTTPException(status_code=404, detail="Plugin not found")
    r.hincrby(f'{settings.redis_prefix}plugin-count', plugin)
    r.hincrby(f'{settings.redis_prefix}plugin-count', 'accumulated')
    return RedirectResponse(f"/File/Get/{plugin_hashed_name}", status_code=302)


@router.get("/PluginMaster", response_class=PrettyJSONResponse)
async def pluginmaster(apiLevel: int = 0, settings: Settings = Depends(get_settings)):
    r = Redis.create_client()
    if not apiLevel:
        apiLevel = settings.plugin_api_level
    apilevel_namespace_map = get_apilevel_namespace_map()
    if apiLevel not in apilevel_namespace_map:
        return HTTPException(status_code=400, detail="API level not supported")
    plugin_namespace = apilevel_namespace_map[apiLevel]
    pluginmaster_str = r.hget(f'{settings.redis_prefix}{plugin_namespace}', 'pluginmaster')
    if not pluginmaster_str:
        raise HTTPException(status_code=404, detail="Pluginmaster not found")
    pluginmaster = json.loads(pluginmaster_str)
    translations = {}
    if settings.default_pm_lang != 'en-US':
        desc_str = r.hget(f'{settings.redis_prefix}crowdin', f'plugin-description-{settings.default_pm_lang}') or '{}'
        punchline_str = r.hget(f'{settings.redis_prefix}crowdin', f'plugin-punchline-{settings.default_pm_lang}') or '{}'
        translations = {
            'description': json.loads(desc_str),
            'punchline': json.loads(punchline_str)
        }
    print(translations)
    for plugin in pluginmaster:
        plugin_name = plugin['InternalName']
        download_count = r.hget(f'{settings.redis_prefix}plugin-count', plugin_name) or 0
        plugin["DownloadCount"] = int(download_count)
        if translations:
            plugin['Description'] = translations['description'].get(plugin_name, plugin.get('Description'))
            plugin['Punchline'] = translations['punchline'].get(plugin_name, plugin.get('Punchline'))
    return pluginmaster


@router.get("/CoreChangelog")
async def core_changelog(settings: Settings = Depends(get_settings)):
    r = Redis.create_client()
    changelog_str = r.hget(f'{settings.redis_prefix}dalamud', 'changelog')
    if not changelog_str:
        return []
    changelog = json.loads(changelog_str)
    return changelog


@router.post("/ClearCache")
async def clear_cache(background_tasks: BackgroundTasks, key: str = Query(), settings: Settings = Depends(get_settings)):
    if key != settings.cache_clear_key:
        raise HTTPException(status_code=400, detail="Cache clear key not match")
    background_tasks.add_task(regen, ['plugin'])
    return {'message': 'Background task was started.'}
