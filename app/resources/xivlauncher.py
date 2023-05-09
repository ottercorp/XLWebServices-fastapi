import re
import json
from typing import Union
from app.config import Settings
from app.utils.common import get_settings
from app.utils.redis import Redis
from app.utils.tasks import regen
from fastapi import APIRouter, HTTPException, Depends, Query, BackgroundTasks
from fastapi.responses import RedirectResponse, PlainTextResponse

router = APIRouter()

SEMVER_REGEX = r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(\.(0|[1-9]\d*))?(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$|^$"

@router.get("/Meta")
async def xivlauncher_meta(settings: Settings = Depends(get_settings)):
    r = Redis.create_client()
    release_meta_str = r.hget(f'{settings.redis_prefix}xivlauncher', 'release-meta')
    release_meta = json.loads(release_meta_str) if release_meta_str else {}
    prerelease_meta_str = r.hget(f'{settings.redis_prefix}xivlauncher', 'prerelease-meta')
    prerelease_meta = json.loads(prerelease_meta_str) if prerelease_meta_str else {}
    total_downloads = r.hget(f'{settings.redis_prefix}xivlauncher-count', 'XLStarts') or 0
    unique_installs = r.hget(f'{settings.redis_prefix}xivlauncher-count', 'XLUniqueInstalls') or 0
    version_info = {
        'totalDownloads': int(total_downloads),
        'uniqueInstalls': int(unique_installs),
        'releaseVersion': release_meta,
        'prereleaseVersion': prerelease_meta,
    }
    return version_info


@router.get("/Update/{track_file:path}")
async def xivlauncher(track_file: str, localVersion: Union[str, None] = None, settings: Settings = Depends(get_settings)):
    if len(track_file.split('/')) != 2:
        return HTTPException(status_code=400, detail="Invalid path")
    track, file = track_file.split('/')
    r = Redis.create_client()
    if localVersion:
        if not re.match(SEMVER_REGEX, localVersion):
            raise HTTPException(status_code=400, detail="Invalid local version")
        if (file == "RELEASES"):
            r.hincrby(f'{settings.redis_prefix}xivlauncher-count', 'XLStarts')
    else:
        if (file == "RELEASES"):
            r.hincrby(f'{settings.redis_prefix}xivlauncher-count', 'XLUniqueInstalls')
    if track == 'Release':
        release_type = 'release'
    elif track == 'Prerelease':
        release_type = 'prerelease'
    else:
        raise HTTPException(status_code=400, detail="Invalid track")

    if file == 'RELEASES':
        releases_list = r.hget(f'{settings.redis_prefix}xivlauncher', f'{release_type}-releaseslist')
        return PlainTextResponse(releases_list)
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
