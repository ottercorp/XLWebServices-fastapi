import os, sys
import json
import codecs
from app.utils import httpx_client
from app.config import Settings
from app.utils.common import get_settings
from app.utils.redis import Redis
from fastapi import APIRouter, HTTPException, Depends, Query, BackgroundTasks
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field

from app.utils.tasks import regen

router = APIRouter()


@router.get("/Asset/Meta")
async def dalamud_assets(settings: Settings = Depends(get_settings)):
    r = Redis.create_client()
    asset_str = r.hget(f'{settings.redis_prefix}asset', 'meta')
    if not asset_str:
        raise HTTPException(status_code=404, detail="Asset meta not found")
    asset_json = json.loads(asset_str)
    return asset_json


@router.get("/Release/VersionInfo")
async def dalamud_release(settings: Settings = Depends(get_settings), track: str = "release"):
    if track == "staging":
        track = "stg"
    if not track:
        track = "release"
    r = Redis.create_client()
    version_str = r.hget(f'{settings.redis_prefix}dalamud', f'dist-{track}')
    if not version_str:
        raise HTTPException(status_code=400, detail="Invalid track")
    version_json = json.loads(version_str)
    return version_json


@router.get("/Release/Meta")
async def dalamud_release_meta(settings: Settings = Depends(get_settings)):
    meta_json = {}
    r = Redis.create_client()
    for track in ['release', 'stg', 'canary']:
        version_str = r.hget(f'{settings.redis_prefix}dalamud', f'dist-{track}')
        if not version_str:
            continue
        version_json = json.loads(version_str)
        meta_json[track] = version_json
    return meta_json


@router.get("/Release/Runtime/{kind_version:path}")
async def dalamud_runtime(kind_version: str, settings: Settings = Depends(get_settings)):
    if len(kind_version.split('/')) != 2:
        return HTTPException(status_code=400, detail="Invalid path")
    kind, version = kind_version.split('/')
    r = Redis.create_client()
    kind_map = {
        'WindowsDesktop': 'desktop',
        'DotNet': 'dotnet',
        'Hashes': 'hashes'
    }
    if kind not in kind_map:
        raise HTTPException(status_code=400, detail="Invalid kind")
    hashed_name = r.hget(f'{settings.redis_prefix}runtime', f'{kind_map[kind]}-{version}')
    if not hashed_name:
        raise HTTPException(status_code=400, detail="Invalid version")
    return RedirectResponse(f"/File/Get/{hashed_name}", status_code=302)


@router.post("/Release/ClearCache")
async def release_clear_cache(background_tasks: BackgroundTasks, key: str = Query(), settings: Settings = Depends(get_settings)):
    if key != settings.cache_clear_key:
        raise HTTPException(status_code=400, detail="Cache clear key not match")
    background_tasks.add_task(regen, ['dalamud', 'dalamud_changelog'])
    return {'message': 'Background task was started.'}


@router.post("/Asset/ClearCache")
async def asset_clear_cache(background_tasks: BackgroundTasks, key: str = Query(), settings: Settings = Depends(get_settings)):
    if key != settings.cache_clear_key:
        raise HTTPException(status_code=400, detail="Cache clear key not match")
    background_tasks.add_task(regen, ['asset'])
    return {'message': 'Background task was started.'}


class Analytics(BaseModel):
    client_id: str
    user_id: str
    server_id: str
    banned_plugin_length: str
    os: str
    dalamud_version:str = ""


api_secret = "CWTvRIdaTJuLmiZjAZ3L9w"
measurement_id = "G-W3HJPGVM1J"


@router.post("/Analytics/Start")
async def analytics_start(analytics: Analytics, settings: Settings = Depends(get_settings)):
    url = f"https://www.google-analytics.com/mp/collect?measurement_id={measurement_id}&api_secret={api_secret}"
    data = {
        "client_id": analytics.client_id,
        "user_id": analytics.user_id,
        "user_properties": {
            "HomeWorld": {
                "value": analytics.server_id
            },
            "Banned_Plugin_Length": {
                "value": analytics.banned_plugin_length
            },
            "Client": {
                "value": analytics.client_id,
            },
            "os":{
                "value": analytics.os,
            },
            "dalamud_version":{
                "value": analytics.dalamud_version if analytics.dalamud_version is not None else ""
            }
        },
        'events': [{
            'name': 'start_dalamud',
            "params": {
                "server_id": analytics.server_id,
                "engagement_time_msec": "100",
                "session_id": analytics.user_id  # 复用user_id，确保会话角色唯一
            }
        }]
    }
    await httpx_client.post(url, json=data)
    return {'message': 'OK'}
