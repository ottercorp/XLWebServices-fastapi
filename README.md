# XLWebServices-fastapi
Yet another xlweb service provider written in python &amp; fastapi

## Progress

- [x] File Caching System
- [x] Dalamud Assets
- [x] Dalamud Runtime
- [x] Dalamud Distribution
- [x] Dalamud Core Changelog (why is it in /Plugin)
- [x] Plugin Master
- [x] Multiple Plugin Master (D17 & old)
- [x] Plugin Download Count
- [x] XIVLauncher Distribution
- [x] XIVLauncher Changelog
- [x] XIVLauncher Download Count
- [ ] Webhook (Discord & OtterBot)
- [ ] Bleatbot

## Use

### Python & Requirements

Developed in Python 3.9.9, better to try Python 3.11.

Install dependencies by `pip install -r requirements.txt`

### Config & Env

Create a `.env` file with env vars like:

```
CACHE_CLEAR_KEY=''
GITHUB_TOKEN=''
DALAMUD_REPO='https://github.com/ottercorp/Dalamud.git'
DISTRIB_REPO='https://github.com/ottercorp/dalamud-distrib.git'
PLUGIN_REPO='https://github.com/ottercorp/PluginDistD17.git'
ASSET_REPO='https://github.com/ottercorp/DalamudAssets.git'
XIVL_REPO='https://github.com/ottercorp/FFXIVQuickLauncher.git'
HOSTED_URL='https://aonyx.ffxiv.wang/'
PLUGIN_API_LEVEL='7'
API_NAMESPACE='{"7": "plugin-PluginDistD17-main"}'
```

For the `*_REPO` vars, both `https://github.com/xxx/yyy.git` and `git@github.com:xxx/yyy.git` are supported.

For other available settings please check [the config file](/app/config/__init__.py).

### Run

`python main.py`

### Caching & Regen

Run `python regen.py` for the first generation, additional parameters can also be added for partial re-generation.

Valid parameters are: `dalamud dalamud_changelog plugin asset xivlauncher`.
