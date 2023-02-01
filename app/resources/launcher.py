from typing import Union
from app.config import Settings
from app.utils.common import get_settings
from app.utils.redis import Redis
from app.utils.tasks import regen
from fastapi import APIRouter, HTTPException, Depends, Query, BackgroundTasks, Header
from fastapi.responses import RedirectResponse
from datetime import datetime, timedelta

router = APIRouter()

SEMVER_REGEX = r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$|^$"


@router.get("/GetLease")
async def launcher(
        user_agent: Union[str, None] = Header(default="XIVLauncher"),
        x_xl_track: Union[str, None] = Header(default="Release"),
        x_xl_lv: Union[str, None] = Header(default="0"),
        x_xl_haveversion: Union[str, None] = Header(default="", regex=SEMVER_REGEX),
        x_xl_haveaddon: Union[str, None] = Header(default="", regex=r"yes|no"),
        x_xl_firststart: Union[str, None] = Header(default="no", regex=r"yes|no"),
        x_xl_havewine: Union[str, None] = Header(default="no", regex=r"yes|no"),
        accept: Union[str, None] = Header(default="*/*"),
        settings: Settings = Depends(get_settings)
):
    r = Redis.create_client()
    if x_xl_track == 'Release':
        release_type = 'release'
    elif x_xl_track == 'Prerelease':
        release_type = 'prerelease'
    else:
        raise HTTPException(status_code=400, detail="Invalid track")
    releases_list = r.hget(f'{settings.redis_prefix}xivlauncher', f'{release_type}-releaseslist')

    if x_xl_firststart == 'yes' or not x_xl_haveversion:
        r.hincrby(f'{settings.redis_prefix}xivlauncher-count', 'XLUniqueInstalls')
    r.hincrby(f'{settings.redis_prefix}xivlauncher-count', 'XLStarts')

    return {
        "success": True,
        "message": None,
        "frontierUrl": r"https://launcher.finalfantasyxiv.com/v620/index.html?rc_lang={0}&time={1}",
        "flags": 0,
        "releasesList": releases_list.lstrip('\ufeff'),
        "validUntil": (datetime.utcnow() + timedelta(days=2)).isoformat(),
    }


@router.get("/GetFile/{file}")
async def launcher_file(
        file: str,
        user_agent: Union[str, None] = Header(default="XIVLauncher"),
        x_xl_track: Union[str, None] = Header(default="Release"),
        x_xl_lv: Union[str, None] = Header(default="0"),
        x_xl_haveversion: Union[str, None] = Header(default="", regex=SEMVER_REGEX),
        x_xl_haveaddon: Union[str, None] = Header(default="", regex=r"yes|no"),
        x_xl_firststart: Union[str, None] = Header(default="no", regex=r"yes|no"),
        x_xl_havewine: Union[str, None] = Header(default="no", regex=r"yes|no"),
        accept: Union[str, None] = Header(default="*/*"),
        settings: Settings = Depends(get_settings)
):
    r = Redis.create_client()
    if x_xl_track == 'Release':
        release_type = 'release'
    elif x_xl_track == 'Prerelease':
        release_type = 'prerelease'
    else:
        raise HTTPException(status_code=400, detail="Invalid track")
    tag_name = r.hget(f'{settings.redis_prefix}xivlauncher', f'{release_type}-tag')
    valid_files = [
        'Setup.exe',
        f'XIVLauncherCN-{tag_name}-delta.nupkg',
        f'XIVLauncherCN-{tag_name}-full.nupkg',
        f'XIVLauncher-{tag_name}-delta.nupkg',
        f'XIVLauncher-{tag_name}-full.nupkg',
        'CHANGELOG.txt'
    ]
    hashed_name = r.hget(f'{settings.redis_prefix}xivlauncher', f'{release_type}-{file}')
    if file not in valid_files or not hashed_name:
        raise HTTPException(status_code=400, detail="Invalid file name")
    return RedirectResponse(f"/File/Get/{hashed_name}", status_code=302)


@router.post("/ClearCache")
async def clear_cache(background_tasks: BackgroundTasks, key: str = Query(), settings: Settings = Depends(get_settings)):
    if key != settings.cache_clear_key:
        raise HTTPException(status_code=400, detail="Cache clear key not match")
    background_tasks.add_task(regen, ['xivlauncher'])
    return {'message': 'Background task was started.'}


@router.get("/Download")
async def xivlauncher_download(settings: Settings = Depends(get_settings)):
    r = Redis.create_client()
    hashed_name = r.hget(f'{settings.redis_prefix}xivlauncher', 'release-Setup.exe')
    return RedirectResponse(f"/File/Get/{hashed_name}", status_code=302)
