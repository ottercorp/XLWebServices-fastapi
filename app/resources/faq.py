from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

template_faq = Jinja2Templates(r"artifact/faq")


@router.get("", response_class=HTMLResponse)
async def faq_home():
    # 返回artifact/index.html页面
    return template_faq.TemplateResponse("index.html", context={'request': {}})

@router.get("/", response_class=HTMLResponse)
async def _faq_home():
    # 返回artifact/index.html页面
    return template_faq.TemplateResponse("index.html", context={'request': {}})

@router.get("/xl_troubleshooting", response_class=HTMLResponse)
async def xl_troubleshooting():
    # 返回artifact/index.html页面
    return template_faq.TemplateResponse("xl_troubleshooting.html", context={'request': {}})

@router.get("/dalamud_troubleshooting", response_class=HTMLResponse)
async def dalamud_troubleshooting():
    # 返回artifact/index.html页面
    return template_faq.TemplateResponse("dalamud_troubleshooting.html", context={'request': {}})

@router.get("/development", response_class=HTMLResponse)
async def development():
    # 返回artifact/index.html页面
    return template_faq.TemplateResponse("development.html", context={'request': {}})

@router.get("/steamdeck", response_class=HTMLResponse)
async def steamdeck():
    # 返回artifact/index.html页面
    return template_faq.TemplateResponse("steamdeck.html", context={'request': {}})

@router.get("/support", response_class=HTMLResponse)
async def support():
    # 返回artifact/index.html页面
    return template_faq.TemplateResponse("support.html", context={'request': {}})
