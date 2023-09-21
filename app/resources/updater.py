# !/usr/bin/env python
# -*- coding: utf-8 -*-
# cython:language_level=3
# @Time    : 2023/9/13 8:25
# @File    : updater.py
import json
from typing import Union
from app.config import Settings
from app.utils.common import get_settings
from app.utils.redis import Redis
from app.utils.tasks import regen
from fastapi import APIRouter, HTTPException, Depends, Query, BackgroundTasks, Header
from fastapi.responses import RedirectResponse,PlainTextResponse
from datetime import datetime, timedelta

router = APIRouter()

SEMVER_REGEX = r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(\.(0|[1-9]\d*))?(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$|^$"


@router.get("/Release/VersionInfo")
async def updater_version_info(
        user_agent: Union[str, None] = Header(default="Injector"),
        accept: Union[str, None] = Header(default="*/*"),
        x_updater_track: Union[str, None] = Header(default="Release"),
        settings: Settings = Depends(get_settings)
):
    r = Redis.create_client()
    if x_updater_track == 'Release':
        release_type = 'release'
    elif x_updater_track == 'Prerelease':
        release_type = 'prerelease'
    else:
        raise HTTPException(status_code=400, detail="Invalid track")
    hashed_name = r.hget(f'{settings.redis_prefix}updater', f'{release_type}-asset')
    version_dict = json.loads(r.hget(f'{settings.redis_prefix}updater', 'version'))
    # if x_xl_firststart == 'yes' or not x_xl_haveversion:
    #     r.hincrby(f'{settings.redis_prefix}xivlauncher-count', 'XLUniqueInstalls')
    # r.hincrby(f'{settings.redis_prefix}xivlauncher-count', 'XLStarts')
    return {
        "version": version_dict[f'{release_type}'],
        "downloadurl": f"https://aonyx.ffxiv.wang/File/Get/{hashed_name}",
        "changelog": 'https://aonyx.ffxiv.wang/Updater/ChangeLog',
        "config":{
            "SafeMode": True,
        }
    }

@router.post("/ClearCache")
async def clear_cache(background_tasks: BackgroundTasks, key: str = Query(), settings: Settings = Depends(get_settings)):
    if key != settings.cache_clear_key:
        raise HTTPException(status_code=400, detail="Cache clear key not match")
    background_tasks.add_task(regen, ['updater'])
    return {'message': 'Background task was started.'}


@router.get("/Download")
async def updater_download(settings: Settings = Depends(get_settings)):
    r = Redis.create_client()
    hashed_name = r.hget(f'{settings.redis_prefix}updater', 'release-asset')
    return RedirectResponse(f"/File/Get/{hashed_name}", status_code=302)


@router.get("/ChangeLog")
async def updater_changelog(settings: Settings = Depends(get_settings)):
    return PlainTextResponse('Updater更新公告\n新增安全模式注入，勾选后可以不启动插件注入，方便更新旧版本插件。')
