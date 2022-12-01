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

Create a `.env` file with env vars like:

```
CACHE_CLEAR_KEY=''
GITHUB_TOKEN=''
DALAMUD_REPO=''
DISTRIB_REPO=''
PLUGIN_REPO=''
ASSET_REPO=''
XIVL_REPO=''
HOSTED_URL=''
PLUGIN_API_LEVEL=''
```

For other available settings please check [the config file](/app/config/__init__.py).
