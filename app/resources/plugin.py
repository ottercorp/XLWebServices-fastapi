import os, sys
import re
import json
import codecs
from functools import cache
from app.config import Settings
from app.util import get_settings, Redis, regen_asset
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse, Response

router = APIRouter()

# may refactor this to configurable
APILEVEL_NAMESPACE_MAP = {
    7: 'plugin-PluginDistD17-main',
    6: 'plugin-DalamudPlugins-cn-api6'
}


@router.get("/Download/{plugin}")
async def plugin_download(plugin: str, isUpdate: bool = False, isTesting: bool = False, branch: str = 'api7'):
    r = Redis.create_client()
    api_level = re.search(r'api(?P<level>\d+)', branch).group('level')
    api_level = int(api_level)
    if api_level not in APILEVEL_NAMESPACE_MAP:
        return HTTPException(status_code=400, detail="API level not supported")
    plugin_namespace = APILEVEL_NAMESPACE_MAP[api_level]
    plugin_name = plugin + '-testing' if isTesting else plugin
    plugin_hashed_name = r.hget(f'xlweb-fastapi|{plugin_namespace}', plugin_name)
    if not plugin_hashed_name and isTesting:  # use stable if testing not exists
        plugin_hashed_name = r.hget(f'xlweb-fastapi|{plugin_namespace}', plugin)
    if not plugin_hashed_name:
        raise HTTPException(status_code=404, detail="Plugin not found")
    return RedirectResponse(f"/File/Get/{plugin_hashed_name}", status_code=302)


class PrettyJSONResponse(Response):
    media_type = "application/json"

    def render(self, content) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=2,
            separators=(", ", ": "),
        ).encode("utf-8")


@router.get("/PluginMaster", response_class=PrettyJSONResponse)
async def pluginmaster(apiLevel: int = 6):
    r = Redis.create_client()
    if apiLevel not in APILEVEL_NAMESPACE_MAP:
        return HTTPException(status_code=400, detail="API level not supported")
    plugin_namespace = APILEVEL_NAMESPACE_MAP[apiLevel]
    pluginmaster_str = r.hget(f'xlweb-fastapi|{plugin_namespace}', 'pluginmaster')
    if not pluginmaster_str:
        pluginmaster = regen_pluginmaster(r)
    else:
        pluginmaster = json.loads(pluginmaster_str)
    return pluginmaster