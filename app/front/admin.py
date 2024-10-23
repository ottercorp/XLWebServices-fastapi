# -*- coding: utf-8 -*-
# cython:language_level=3
import asyncio
import json
import secrets
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Depends, Query, BackgroundTasks, Request
from fastapi.responses import RedirectResponse, PlainTextResponse, HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates

from app.utils import httpx_client
from app.config import Settings
from app.utils.common import get_settings, get_tos_content, get_tos_hash
from app.utils.front import flash
from app.utils.tasks import regen
from app.utils.redis import Redis, RedisFeedBack

router = APIRouter()
template = Jinja2Templates("templates")


# region admin index page
@router.get('/', response_class=HTMLResponse)
async def front_admin_index(request: Request):
    return template.TemplateResponse("admin_index.html", {"request": request})


async def run_command(command):
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()

    if process.returncode == 0:
        return stdout.decode().strip()
    else:
        raise RuntimeError(f"Command failed with return code {process.returncode}: {stderr.decode().strip()}")


@router.get('/download_logs', response_class=PlainTextResponse)
async def front_admin_download_logs():
    result = await run_command("journalctl -xeu XLWeb-fastapi")
    log_path = r'./logs/XLWebServices.log'
    with open(log_path, 'w') as f:
        f.write(result)
    return FileResponse(log_path)


@router.get('/stop_svr')
async def front_admin_stop():
    await run_command("systemctl stop XLWeb-fastapi")
    return


@router.get('/restart_svr')
async def front_admin_restart():
    await run_command("systemctl restart XLWeb-fastapi")
    return


@router.get('/update_svr')
async def front_admin_update():
    await run_command("update_XLWeb")
    return


# endregion

# region feedback
@router.get('/feedback', response_class=HTMLResponse)
async def front_admin_feedback_get(request: Request):
    r = Redis.create_client()
    r_fb = RedisFeedBack.create_client()
    feedback_list = r_fb.keys('feedback|*')
    return_list = []
    for i in feedback_list:
        temp_list = i.replace('feedback|', '').split('|')
        return_list.append(temp_list)
    return template.TemplateResponse("feedback_admin.html", {"request": request, "feedback_list": return_list})

@router.get('/feedback/detail/{plugin_name}/{feedback_id}', response_class=HTMLResponse)
async def front_admin_feedback_detail_get(request: Request, plugin_name: str, feedback_id: int, dhash: str):
    r = Redis.create_client()
    feedback = r.hgetall(f'feedback|{plugin_name}|{feedback_id}')
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    feedback['reply_log'] = json.loads(feedback['reply_log'])
    return template.TemplateResponse("feedback_admin_detail.html", {"request": request, "feedback": feedback})

# endregion

@router.get('/flush', response_class=HTMLResponse)
async def front_admin_flush_get(request: Request):
    return template.TemplateResponse("flush.html", {"request": request})


@router.post('/flush')
async def front_admin_flush_post(request: Request):
    flash(request, 'error', '测试', )
    return template.TemplateResponse("flush.html", {"request": request})


@router.get('/flush_cache')
async def front_admin_flush_cache_get(request: Request, task: str | None = None):
    if task:
        match task:
            case 'dalamud':
                regen(['dalamud', 'dalamud_changelog'])
            case 'asset':
                regen(['asset'])
            case 'plugin':
                regen(['plugin'])
            case 'xivlauncher':
                regen(['xivlauncher'])
            case 'updater':
                regen(['updater'])
            case 'xlassets':
                regen(['xlassets'])
            case 'all':
                regen(['dalamud', 'dalamud_changelog', 'asset', 'plugin', 'xivlauncher', 'updater', 'xlassets'])
            case _:
                flash(request, 'error', '任务不存在', )

    if request.headers.get('referer') and 'flush' in request.headers.get('referer'):
        return RedirectResponse(url=router.url_path_for("front_admin_flush_get"))
    else:
        return RedirectResponse(url=router.url_path_for("front_admin_index"))
