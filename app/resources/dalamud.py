import os, sys
import json
import codecs
from app.config import Settings
from app.util import get_settings, Redis, regen_asset
from fastapi import APIRouter, HTTPException, Depends

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
    return {}

@router.get("/Release/Runtime/DotNet/{version}")
async def dalamud_runtime_dotnet(settings: Settings = Depends(get_settings)):
    return {}

@router.get("/Release/Runtime/WindowsDesktop/{version}")
async def dalamud_runtime_windowsdesktop(settings: Settings = Depends(get_settings)):
    return {}


