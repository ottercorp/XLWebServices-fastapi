# -*- coding: utf-8 -*-
# cython:language_level=3
import secrets

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from .admin import router as admin_router
from ..config import Settings
from ..utils.common import get_settings

router = APIRouter()
security = HTTPBasic()


async def verify_admin(settings: Settings = Depends(get_settings), credentials: HTTPBasicCredentials = Depends(security)):
    # 比较用户名和密码
    correct_username = secrets.compare_digest(credentials.username, settings.admin_user_name)
    correct_password = secrets.compare_digest(credentials.password, settings.admin_user_pwd)

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


router.include_router(admin_router, prefix='/admin', dependencies=[Depends(verify_admin)])
