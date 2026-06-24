# -*- coding: utf-8 -*-
# cython:language_level=3
import asyncio
import json
from datetime import datetime, timezone, timedelta
from io import BytesIO

from fastapi import APIRouter, HTTPException, Depends, Request, Form, UploadFile
from fastapi.responses import RedirectResponse, PlainTextResponse, HTMLResponse, FileResponse, Response, JSONResponse
from fastapi.templating import Jinja2Templates

from app.config import Settings
from app.utils.cdn.ottercloudcdn import OtterCloudCDN
from app.utils.common import get_settings, get_apilevel_namespace_map
from app.utils.dalamud_log_analysis import analysis
from app.utils.front import flash
from app.utils.redis import RedisFeedBack, Redis
from app.utils.tasks import regen, flush_stg_code

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


@router.get('/stg_code')
async def front_admin_stg_code(request: Request):
    r = Redis.create_client()
    settings = get_settings()
    stg_code = r.hget(f'{settings.redis_prefix}settings', 'stg_code')
    flash(request, 'info', f'Stg Code为 {stg_code}')
    return RedirectResponse(url=request.app.url_path_for("front_admin_index"), status_code=303)


# endregion

# region feedback
@router.get('/feedback', response_class=HTMLResponse)
async def front_admin_feedback_get(request: Request):
    r_fb = RedisFeedBack.create_client()
    feedback_list = r_fb.keys('feedback|*')
    return_list = []
    for i in feedback_list:
        temp_list = i.replace('feedback|', '').split('|')
        return_list.append(temp_list)
    return template.TemplateResponse("feedback_admin.html", {"request": request, "feedback_list": return_list})


@router.get('/feedback/export', response_class=HTMLResponse)
async def front_admin_feedback_export_get(request: Request):
    r_fb = RedisFeedBack.create_client()
    feedback_list = r_fb.keys('feedback|*')
    return_dict = {}
    for i in feedback_list:
        dhash, plugin_name, order_id = i.replace('feedback|', '').split('|')
        if plugin_name not in return_dict:
            return_dict[plugin_name] = []
        feedback = r_fb.hgetall(f'feedback|{dhash}|{plugin_name}|{order_id}')
        create_time = datetime.fromtimestamp(float(feedback.get('create_time', 0)), tz=timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M:%S')
        return_dict[plugin_name].append({
            "order_id": order_id,
            "dhash": dhash,
            "version": feedback['version'],
            "content": feedback['content'],
            "exception": feedback['exception'],
            "reporter": feedback['reporter'],
            "create_time": create_time,
        })
    for k, v in return_dict.items():
        return_dict[k] = sorted(v, key=lambda x: x['order_id'], reverse=True)
    return template.TemplateResponse("feedback_export.html", {"request": request, "export_dict": return_dict})


@router.get('/feedback/detail/{plugin_name}/{feedback_id}', response_class=HTMLResponse)
async def front_admin_feedback_detail_get(request: Request, plugin_name: str, feedback_id: int, dhash: str | None = None):
    r_fb = RedisFeedBack.create_client()
    feedback = r_fb.hgetall(f'feedback|{dhash}|{plugin_name}|{feedback_id}')
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    feedback['reply_log'] = json.loads(feedback['reply_log'])
    feedback['create_time'] = datetime.fromtimestamp(float(feedback.get('create_time', 0)), tz=timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M:%S')
    return template.TemplateResponse("feedback_admin_detail.html", {"request": request, "detail": feedback, "plugin_name": plugin_name, "feedback_id": feedback_id})


@router.get('/feedback/solve/{feedback_id}', response_class=RedirectResponse)
async def front_admin_feedback_solve_get(request: Request, feedback_id: int, referer: str | None = None):
    r_fb = RedisFeedBack.create_client()
    feedback_list = r_fb.keys(f'feedback|*|{feedback_id}')
    if len(feedback_list) == 1:
        r_fb.delete(feedback_list[0])
        if referer == "export":
            return RedirectResponse(request.app.url_path_for('front_admin_feedback_export_get'))
        else:
            return RedirectResponse(request.app.url_path_for('front_admin_feedback_get'))
    elif len(feedback_list) > 1:
        raise HTTPException(status_code=400, detail="More than one feedback found.")
    else:
        raise HTTPException(status_code=400, detail="No feedback found.")


@router.post('/feedback/reply/{feedback_id}', response_class=RedirectResponse)
async def front_admin_feedback_reply_post(request: Request, feedback_id: int, content: str):
    raise HTTPException(status_code=404, detail="Not implemented yet.")


# endregion

# region flush
@router.get('/flush', response_class=HTMLResponse)
async def front_admin_flush_get(request: Request):
    return template.TemplateResponse("flush.html", {"request": request})


@router.post('/flush')
async def front_admin_flush_post(request: Request, action: str = Form(...), task_type: int = Form(...), content: str = Form(...), ottercloudcdn: OtterCloudCDN = Depends(OtterCloudCDN)):
    try:
        url_list = content.replace('\r', '').split('\n')
        if action == 'prefetch':
            ottercloudcdn.prefetch(task_type, url_list)
            flash(request, 'success', f'预取任务已提交')
        if action == 'flushUrl':
            ottercloudcdn.refresh(task_type, url_list)
            flash(request, 'success', f'刷新任务已完成')
    except Exception as e:
        flash(request, 'error', f'任务失败，{e}', )
    finally:
        return RedirectResponse(url=request.app.url_path_for('front_admin_flush_get'), status_code=303)


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
                return RedirectResponse(url=request.app.url_path_for("front_admin_flush_get"))
        flash(request, 'success', f'刷新{task if task != "all" else "全部"}任务已完成')
    else:
        raise HTTPException(status_code=400, detail="No task specified.")
    if request.headers.get('referer') and 'flush' in request.headers.get('referer'):
        return RedirectResponse(url=request.app.url_path_for("front_admin_flush_get"), status_code=303)
    else:
        return RedirectResponse(url=request.app.url_path_for("front_admin_index"), status_code=303)


@router.get('/flush_stg_code')
async def front_admin_flush_stg_code(request: Request):
    stg_code = flush_stg_code()
    flash(request, 'success', f'刷新Stg Code已完成，新的key为 {stg_code}')
    if request.headers.get('referer') and 'flush' in request.headers.get('referer'):
        return RedirectResponse(url=request.app.url_path_for("front_admin_flush_get"), status_code=303)
    else:
        return RedirectResponse(url=request.app.url_path_for("front_admin_index"), status_code=303)


# endregion

# region analytics
@router.get('/log_analytics', response_class=HTMLResponse)
async def front_admin_log_analytics_get(request: Request):
    return template.TemplateResponse("log_analysis.html", {"request": request})


@router.post('/log_analytics', )
async def front_admin_log_analytics_post(request: Request, file: UploadFile = Form(...), settings: Settings = Depends(get_settings)):
    file_byte = await file.read()
    file = BytesIO(file_byte)
    analysis_result, log_file_type = analysis(file, settings.plugin_api_level)
    return template.TemplateResponse("log_analysis_result.html", {"request": request, "analysis_result": analysis_result, "log_file_type": log_file_type})

# endregion

# region plugin translations
def _load_pluginmaster():
    r = Redis.create_client()
    settings = get_settings()
    apilevel_namespace_map = get_apilevel_namespace_map()
    plugin_namespace = apilevel_namespace_map.get(settings.plugin_api_level)
    pluginmaster_str = r.hget(f'{settings.redis_prefix}{plugin_namespace}', 'pluginmaster')
    return json.loads(pluginmaster_str) if pluginmaster_str else []


@router.get('/plugins', response_class=HTMLResponse)
async def front_admin_plugins_get(request: Request, settings: Settings = Depends(get_settings)):
    r = Redis.create_client()
    lang = settings.default_pm_lang
    pluginmaster = _load_pluginmaster()
    name_tr = json.loads(r.hget(f'{settings.redis_prefix}crowdin', f'plugin-name-{lang}') or '{}')
    desc_tr = json.loads(r.hget(f'{settings.redis_prefix}crowdin', f'plugin-description-{lang}') or '{}')
    punch_tr = json.loads(r.hget(f'{settings.redis_prefix}crowdin', f'plugin-punchline-{lang}') or '{}')
    plugins = []
    for p in pluginmaster:
        internal_name = p.get('InternalName', '')
        last_update = int(p.get('LastUpdate', 0) or 0)
        download_count = r.hget(f'{settings.redis_prefix}plugin-count', internal_name)
        download_count = int(download_count) if download_count else int(p.get('DownloadCount', 0) or 0)
        last_update_str = ''
        if last_update:
            last_update_str = datetime.fromtimestamp(
                last_update, tz=timezone(timedelta(hours=8))
            ).strftime('%Y-%m-%d')
        plugins.append({
            'internal_name': internal_name,
            'name': p.get('Name', ''),
            'description': p.get('Description', ''),
            'punchline': p.get('Punchline', ''),
            'icon_url': p.get('IconUrl', ''),
            't_name': name_tr.get(internal_name, ''),
            't_description': desc_tr.get(internal_name, ''),
            't_punchline': punch_tr.get(internal_name, ''),
            'version': p.get('AssemblyVersion', ''),
            'api_level': p.get('DalamudApiLevel', ''),
            'download_count': download_count,
            'last_update': last_update,
            'last_update_str': last_update_str,
            'cn_maintained': bool(p.get('_cn', False)),
            'upstream_version': p.get('_uv', ''),
            'repo_url': p.get('RepoUrl', '') or '',
        })
    plugins.sort(key=lambda x: x['name'].lower())
    api_levels = [int(p['api_level']) for p in plugins if str(p['api_level']).strip().isdigit()]
    max_api_level = max(api_levels) if api_levels else 0
    for p in plugins:
        if str(p['api_level']).strip().isdigit():
            behind = max_api_level - int(p['api_level'])
        else:
            behind = 0
        p['outdated'] = behind >= 1
        p['very_outdated'] = behind > 1
    return template.TemplateResponse("plugins.html", {"request": request, "plugins": plugins, "lang": lang, "max_api_level": max_api_level})


@router.get('/plugins/download_all')
async def front_admin_plugins_download_all():
    items = []
    for p in _load_pluginmaster():
        items.append({
            'InternalName': p.get('InternalName', ''),
            'Name': p.get('Name', ''),
            'Punchline': p.get('Punchline', ''),
            'Description': p.get('Description', ''),
        })
    content = json.dumps(items, ensure_ascii=False, indent=2)
    return Response(
        content=content,
        media_type='application/json',
        headers={'Content-Disposition': 'attachment; filename="plugins_all.json"'}
    )


@router.get('/plugins/download_all_translated')
async def front_admin_plugins_download_all_translated(settings: Settings = Depends(get_settings)):
    r = Redis.create_client()
    lang = settings.default_pm_lang
    name_tr = json.loads(r.hget(f'{settings.redis_prefix}crowdin', f'plugin-name-{lang}') or '{}')
    desc_tr = json.loads(r.hget(f'{settings.redis_prefix}crowdin', f'plugin-description-{lang}') or '{}')
    punch_tr = json.loads(r.hget(f'{settings.redis_prefix}crowdin', f'plugin-punchline-{lang}') or '{}')
    items = []
    for p in _load_pluginmaster():
        internal_name = p.get('InternalName', '')
        items.append({
            'InternalName': internal_name,
            'Name': name_tr.get(internal_name, ''),
            'Punchline': punch_tr.get(internal_name, ''),
            'Description': desc_tr.get(internal_name, ''),
            '_Original': {
                'Name': p.get('Name', ''),
                'Punchline': p.get('Punchline', ''),
                'Description': p.get('Description', ''),
            },
        })
    content = json.dumps(items, ensure_ascii=False, indent=2)
    return Response(
        content=content,
        media_type='application/json',
        headers={'Content-Disposition': f'attachment; filename="plugins_translated_{lang}.json"'}
    )


@router.post('/plugins/upload_all')
async def front_admin_plugins_upload_all(request: Request, lang: str = Form(...), file: UploadFile = Form(...), settings: Settings = Depends(get_settings)):
    lang = lang.strip()
    if not lang:
        flash(request, 'error', '语言不能为空')
        return RedirectResponse(url=request.app.url_path_for('front_admin_plugins_get'), status_code=303)
    try:
        raw = await file.read()
        data = json.loads(raw.decode('utf-8-sig'))
        if not isinstance(data, list):
            raise ValueError('整合 JSON 顶层必须是数组，每个 item 含 InternalName / Name / Punchline / Description')
        field_maps = {'name': {}, 'punchline': {}, 'description': {}}
        for item in data:
            if not isinstance(item, dict):
                continue
            internal = item.get('InternalName')
            if not internal:
                continue
            for field, src_key in (('name', 'Name'), ('punchline', 'Punchline'), ('description', 'Description')):
                value = item.get(src_key)
                if value:
                    field_maps[field][internal] = value
        r = Redis.create_client()
        counts = {}
        for field, new_map in field_maps.items():
            existing = json.loads(r.hget(f'{settings.redis_prefix}crowdin', f'plugin-{field}-{lang}') or '{}')
            existing.update(new_map)
            r.hset(f'{settings.redis_prefix}crowdin', f'plugin-{field}-{lang}', json.dumps(existing, ensure_ascii=False))
            counts[field] = len(new_map)
        flash(request, 'success', f'已上传 {lang} 整合翻译：Name {counts["name"]} 条、Punchline {counts["punchline"]} 条、Description {counts["description"]} 条')
    except Exception as e:
        flash(request, 'error', f'上传失败：{e}')
    return RedirectResponse(url=request.app.url_path_for('front_admin_plugins_get'), status_code=303)


@router.post('/plugins/edit')
async def front_admin_plugins_edit(request: Request, internal_name: str = Form(...), lang: str = Form(...), name: str = Form(''), punchline: str = Form(''), description: str = Form(''), settings: Settings = Depends(get_settings)):
    lang = lang.strip()
    if not lang:
        return JSONResponse({'ok': False, 'error': '语言为空'}, status_code=400)
    if not internal_name:
        return JSONResponse({'ok': False, 'error': '缺少 InternalName'}, status_code=400)
    try:
        r = Redis.create_client()
        hkey = f'{settings.redis_prefix}crowdin'
        result = {}
        for field, value in (('name', name), ('punchline', punchline), ('description', description)):
            value = value.strip()
            fkey = f'plugin-{field}-{lang}'
            field_map = json.loads(r.hget(hkey, fkey) or '{}')
            if value:
                field_map[internal_name] = value
            else:
                field_map.pop(internal_name, None)
            r.hset(hkey, fkey, json.dumps(field_map, ensure_ascii=False))
            result[field] = value
        return JSONResponse({'ok': True, **result})
    except Exception as e:
        return JSONResponse({'ok': False, 'error': str(e)}, status_code=500)

# endregion
