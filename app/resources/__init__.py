from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from .dalamud import router as router_dalamud
from .file import router as router_file
from .plugin import router as router_plugin
from .xivlauncher import router as router_xivl
from .launcher import router as router_launcher

from app.utils.git import get_git_hash


router = APIRouter()

router.include_router(router_file, tags=["file"], prefix="/File")
router.include_router(router_dalamud, tags=["dalamud"], prefix="/Dalamud")
router.include_router(router_plugin, tags=["plugin"], prefix="/Plugin")
router.include_router(router_xivl, tags=["xivlauncher"], prefix="/Proxy")
router.include_router(router_launcher, tags=["launcher"], prefix="/Launcher")

@router.get("/", response_class=HTMLResponse)
async def home():
    return f"""
    <h1>XL Web Services -- FastAPI</h1>
    This server provides updates for XIVLauncher and the plugin listing for Dalamud.<br>
    <a href=\"https://goatcorp.github.io/faq/xl_troubleshooting#q-are-xivlauncher-dalamud-and-dalamud-plugins-safe-to-use\">Read more here.</a>
    <br><br>Version: {get_git_hash()}
    """