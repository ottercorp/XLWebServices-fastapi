from typing import Annotated
from fastapi import Depends, FastAPI, Header, HTTPException
from .common import get_settings


def check_auth(key: str) -> bool:
    settings = get_settings()
    return key == settings.plogon_api_key

async def check_auth_header(x_xl_key: Annotated[str, Header()]):
    settings = get_settings()
    if not check_auth(x_xl_key):
        raise HTTPException(status_code=401, detail="Unauthorized")