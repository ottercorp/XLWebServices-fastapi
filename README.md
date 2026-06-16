# XLWebServices-fastapi
Yet another xlweb service provider written in python &amp; fastapi

## Progress

- [x] File Caching System
- [x] Dalamud Assets
- [x] Dalamud Runtime
- [x] Dalamud Distribution
- [x] Dalamud Core Changelog
- [x] Plugin Master
- [x] Multiple Plugin Master (D17 & old)
- [x] Plugin Download Count
- [x] S3-compatible plugin asset upload
- [x] XIVLauncher Distribution
- [x] XIVLauncher Changelog
- [x] XIVLauncher Download Count
- [x] CDN Refresh (CF, CTCDN)
- [x] Crowdin (translation for plugin description & punchline)
- [ ] Webhook (Discord & OtterBot)
- [ ] Bleatbot

## Use

### Python & Requirements

Developed in Python 3.10.4, better to try Python 3.11.

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

# Optional: S3-compatible storage for plugin icons and plugin helper files.
# Leave all three values empty to disable upload.
XIVLAUNCHER_S3_ACCESS_KEY=''
XIVLAUNCHER_S3_SECRET_KEY=''
XIVLAUNCHER_S3_ENDPOINT=''
```

For the `*_REPO` vars, both `https://github.com/xxx/yyy.git` and `git@github.com:xxx/yyy.git` are supported.

For other available settings please check [the config file](/app/config/__init__.py).

#### S3-compatible plugin asset upload

When `XIVLAUNCHER_S3_ACCESS_KEY`, `XIVLAUNCHER_S3_SECRET_KEY`, and `XIVLAUNCHER_S3_ENDPOINT` are all empty, S3 upload is skipped.

When one of them is set, all three must be set. The service creates a path-style S3 client and uploads during `plugin` regeneration:

- plugin icons from `stable/<plugin>/images/icon.png` and `testing-live/<plugin>/images/icon.png` to `s3://plugindistd17/<same relative path>`;
- plugin helper files to `s3://xlassets/pluginfiles/`:
  - `DamageInfoPlugin.csv`;
  - `AggroDistances.dat`.

The endpoint should be the S3 API endpoint, for example:

```
XIVLAUNCHER_S3_ENDPOINT='https://example-account.r2.cloudflarestorage.com'
```

### Run

`python main.py`

### Caching & Regen

Run `python regen.py` for the first generation, additional parameters can also be added for partial re-generation.

Valid parameters are: `dalamud dalamud_changelog plugin asset xivlauncher`.
