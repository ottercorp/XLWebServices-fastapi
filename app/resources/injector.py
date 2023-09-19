# !/usr/bin/env python
# -*- coding: utf-8 -*-
# cython:language_level=3
# @Time    : 2023/9/13 8:25
# @File    : injector.py

from typing import Union
from app.config import Settings
from app.utils.common import get_settings
from app.utils.redis import Redis
from app.utils.tasks import regen
from fastapi import APIRouter, HTTPException, Depends, Query, BackgroundTasks, Header
from fastapi.responses import RedirectResponse
from datetime import datetime, timedelta

router = APIRouter()

SEMVER_REGEX = r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(\.(0|[1-9]\d*))?(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$|^$"


@router.get("/Release/VersionInfo")
async def launcher(
        user_agent: Union[str, None] = Header(default="Injector"),
        accept: Union[str, None] = Header(default="*/*"),
        x_injector_track: Union[str, None] = Header(default="Release"),
        settings: Settings = Depends(get_settings)
):
    r = Redis.create_client()
    if x_injector_track == 'Release':
        release_type = 'release'
    elif x_injector_track == 'Prerelease':
        release_type = 'prerelease'
    else:
        raise HTTPException(status_code=400, detail="Invalid track")
    hashed_name = r.hget(f'{settings.redis_prefix}injector', f'{release_type}-asset')
    version_dict = r.hget(f'{settings.redis_prefix}injector', 'version')
    # if x_xl_firststart == 'yes' or not x_xl_haveversion:
    #     r.hincrby(f'{settings.redis_prefix}xivlauncher-count', 'XLUniqueInstalls')
    # r.hincrby(f'{settings.redis_prefix}xivlauncher-count', 'XLStarts')
    return {
        "success": True,
        "message": None,
        "release":{
            "version": version_dict['release_type'],
            "url": f"/File/Get/{hashed_name}",
        },
        "flags": 0,
    }

@router.post("/ClearCache")
async def clear_cache(background_tasks: BackgroundTasks, key: str = Query(), settings: Settings = Depends(get_settings)):
    if key != settings.cache_clear_key:
        raise HTTPException(status_code=400, detail="Cache clear key not match")
    background_tasks.add_task(regen, ['injector'])
    return {'message': 'Background task was started.'}


@router.get("/Download")
async def xivlauncher_download(settings: Settings = Depends(get_settings)):
    r = Redis.create_client()
    hashed_name = r.hget(f'{settings.redis_prefix}injector', 'release-asset')
    return RedirectResponse(f"/File/Get/{hashed_name}", status_code=302)
