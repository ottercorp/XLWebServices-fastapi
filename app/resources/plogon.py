from app.config import Settings
from app.utils.common import get_settings
from app.utils.redis import Redis
from app.utils.auth import check_auth
from fastapi import APIRouter, HTTPException, Depends


router = APIRouter()


@router.post("/RegisterMessageId")
async def register_message_id(
    key: str,
    prNumber: str,
    messageId: str,
    settings: Settings = Depends(get_settings),
):
    if not check_auth(key):
        raise HTTPException(status_code=401, detail="Unauthorized")
    r = Redis.create_client()
    r.rpush(f'{settings.redis_prefix}plogon|MSGS-{prNumber}', messageId)
    return {'message': 'OK'}


@router.get("/GetMessageIds")
async def get_message_ids(prNumber: str, settings: Settings = Depends(get_settings)):
    r = Redis.create_client()
    ids = r.lrange(f'{settings.redis_prefix}plogon|MSGS-{prNumber}', 0, -1) or []
    return ids


@router.post("/RegisterVersionPrNumber")
async def register_version_pr_number(
    key: str,
    internalName: str,
    version: str,
    prNumber: str,
    settings: Settings = Depends(get_settings),
):
    if not check_auth(key):
        raise HTTPException(status_code=401, detail="Unauthorized")
    r = Redis.create_client()
    r.hset(f'{settings.redis_prefix}plogon|CHANGELOG', f"{internalName}-{version}", prNumber)
    return {'message': 'OK'}

@router.get("/GetVersionChangelog")
async def get_version_changelog(internalName: str, version: str, settings: Settings = Depends(get_settings)):
    r = Redis.create_client()
    pr_number = r.hget(f'{settings.redis_prefix}plogon|CHANGELOG', f"{internalName}-{version}")
    if not pr_number:
        raise HTTPException(status_code=404, detail="Not Found")
    return pr_number
