import os, sys
import json
import codecs
from app.config import Settings
from app.utils.common import get_settings
from app.utils.redis import Redis
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse, PlainTextResponse

router = APIRouter()

@router.get("/Meta")
async def xivlauncher_meta(settings: Settings = Depends(get_settings)):
    r = Redis.create_client()
    release_meta_str = r.hget('xlweb-fastapi|xivlauncher', 'release-meta')
    release_meta = json.loads(release_meta_str) if release_meta_str else {}
    prerelease_meta_str = r.hget('xlweb-fastapi|xivlauncher', 'prerelease-meta')
    prerelease_meta = json.loads(prerelease_meta_str) if prerelease_meta_str else {}
    version_info = {
        'totalDownloads': 0,  # TODO
        'uniqueInstalls': 0,  # TODO
        'releaseVersion': release_meta,
        'prereleaseVersion': prerelease_meta,
    }
    return version_info



@router.get("/Update/{track_file:path}")
async def xivlauncher(track_file: str, settings: Settings = Depends(get_settings)):
    print(track_file)
    if len(track_file.split('/')) != 2:
        return HTTPException(status_code=400, detail="Invalid path")
    track, file = track_file.split('/')
    r = Redis.create_client()
    if track == 'Release':
        release_type = 'release'
    elif track == 'Prerelease':
        release_type = 'prerelease'
    else:
        raise HTTPException(status_code=400, detail="Invalid track")

    if file == 'RELEASES':
        releases_list = r.hget('xlweb-fastapi|xivlauncher', f'{release_type}-releaseslist')
        return PlainTextResponse(releases_list)
    tag_name = r.hget('xlweb-fastapi|xivlauncher', f'{release_type}-tag')

    valid_files = [
        'Setup.exe',
        f'XIVLauncherCN-{tag_name}-delta.nupkg',
        f'XIVLauncherCN-{tag_name}-full.nupkg',
        f'XIVLauncher-{tag_name}-delta.nupkg',
        f'XIVLauncher-{tag_name}-full.nupkg',
        'CHANGELOG.txt'
    ]
    hashed_name = r.hget('xlweb-fastapi|xivlauncher', f'{release_type}-{file}')
    if file not in valid_files or not hashed_name:
        raise HTTPException(status_code=400, detail="Invalid file name")
    return RedirectResponse(f"/File/Get/{hashed_name}", status_code=302)

