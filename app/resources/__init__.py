import json

from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .dalamud import router as router_dalamud
from .file import router as router_file
from .plugin import router as router_plugin
from .xivlauncher import router as router_xivl
from .launcher import router as router_launcher
from .plogon import router as router_plogon
from .faq import router as router_faq
from app.utils.common import get_settings

router = APIRouter()

router.include_router(router_file, tags=["file"], prefix="/File")
router.include_router(router_dalamud, tags=["dalamud"], prefix="/Dalamud")
router.include_router(router_plugin, tags=["plugin"], prefix="/Plugin")
router.include_router(router_xivl, tags=["xivlauncher"], prefix="/Proxy")
router.include_router(router_launcher, tags=["launcher"], prefix="/Launcher")
router.include_router(router_plogon, tags=["plogon"], prefix="/Plogon")
router.include_router(router_faq, tags=["faq"], prefix="/faq")

# @router.get("/", response_class=HTMLResponse)
# async def home():
#     return f"""
#     <h1>XL Web Services -- FastAPI</h1>
#     This server provides updates for XIVLauncher and the plugin listing for Dalamud.<br>
#     <a href=\"https://goatcorp.github.io/faq/xl_troubleshooting#q-are-xivlauncher-dalamud-and-dalamud-plugins-safe-to-use\">Read more here.</a>
#     <br><br>Version: {get_git_hash()}
#     """
template = Jinja2Templates("artifact")


@router.get("/", response_class=HTMLResponse)
async def home():
    # 返回artifact/index.html页面
    return template.TemplateResponse("index.html", context={'request': {}})


@router.get(f"/{get_settings().otterbot_web_json}.json")
async def otterbot_web_json():
    return json.dumps({"bot_appid": get_settings().otterbot_web_json})
