import os, sys
import json
import codecs
from app.config import Settings
from app.utils.common import get_settings
from app.utils.redis import Redis
from app.utils.tasks import regen_asset
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse

router = APIRouter()

@router.get("/Asset/Meta")
async def dalamud_assets(settings: Settings = Depends(get_settings)):
    r = Redis.create_client()
    asset_str = r.hget('xlweb-fastapi|asset', 'meta')
    if not asset_str:
        asset_json = regen_asset(r)
    else:
        asset_json = json.loads(asset_str)
    return asset_json


@router.get("/Release/VersionInfo")
async def dalamud_release(settings: Settings = Depends(get_settings), track: str = "release"):
    if track == "staging":
        track = "stg"
    r = Redis.create_client()
    version_str = r.hget('xlweb-fastapi|dalamud', f'dist-{track}')
    if not version_str:
        raise HTTPException(status_code=400, detail="Invalid track")
    version_json = json.loads(version_str)
    return version_json


@router.get("/Release/Runtime/{kind_version:path}")
async def dalamud_runtime(kind_version: str, settings: Settings = Depends(get_settings)):
    print(kind_version)
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
    hashed_name = r.hget('xlweb-fastapi|runtime', f'{kind_map[kind]}-{version}')
    if not hashed_name:
        raise HTTPException(status_code=400, detail="Invalid version")
    return RedirectResponse(f"/File/Get/{hashed_name}", status_code=302)

