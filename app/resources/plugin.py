import os, sys
import re
import json
import codecs
from functools import cache
from app.config import Settings
from app.utils.common import get_settings
from app.utils.responses import PrettyJSONResponse
from app.utils.redis import Redis
from app.utils.tasks import regen
from fastapi import APIRouter, HTTPException, Depends, Query, BackgroundTasks
from fastapi.responses import RedirectResponse

router = APIRouter()

# may refactor this to configurable
APILEVEL_NAMESPACE_MAP = {
    "7": 'plugin-PluginDistD17-main',
    "6": 'plugin-DalamudPlugins-cn-api6'
}


@router.get("/Download/{plugin}")
async def plugin_download(plugin: str, isUpdate: bool = False, isTesting: bool = False, branch: str = '', settings: Settings = Depends(get_settings)):
    r = Redis.create_client()
    api_level = re.search(r'api(?P<level>.+)', branch).group('level')
    if not api_level:
        api_level = settings.plugin_api_level
    if api_level not in APILEVEL_NAMESPACE_MAP:
        return HTTPException(status_code=400, detail="API level not supported")
    plugin_namespace = APILEVEL_NAMESPACE_MAP[api_level]
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
async def pluginmaster(apiLevel: str = "", settings: Settings = Depends(get_settings)):
    r = Redis.create_client()
    if not apiLevel:
        apiLevel = settings.plugin_api_level
    if apiLevel not in APILEVEL_NAMESPACE_MAP:
        return HTTPException(status_code=400, detail="API level not supported")
    plugin_namespace = APILEVEL_NAMESPACE_MAP[apiLevel]
    pluginmaster_str = r.hget(f'{settings.redis_prefix}{plugin_namespace}', 'pluginmaster')
    if not pluginmaster_str:
        raise HTTPException(status_code=404, detail="Pluginmaster not found")
    pluginmaster = json.loads(pluginmaster_str)
    return pluginmaster


@router.post("/ClearCache")
async def clear_cache(background_tasks: BackgroundTasks, key: str = Query(), settings: Settings = Depends(get_settings)):
    if key != settings.cache_clear_key:
        raise HTTPException(status_code=400, detail="Cache clear key not match")
    background_tasks.add_task(regen, ['plugin'])
    return {'message': 'Background task was started.'}
