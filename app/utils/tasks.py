import os
import re
import json
import shutil
import redis
import codecs
import hashlib
from .common import get_settings, cache_file, download_file
from .git import update_git_repo, get_repo_dir
from .redis import Redis


async def rehash(repo_name_list: list[str]):
    settings = get_settings()
    redis_client = Redis.create_client()
    async for repo in repo_name_list:
        if repo == 'dalamud':
            pass
        elif repo == 'plugin':
            regen_pluginmaster(redis_client)
        elif repo == 'asset':
            regen_asset(redis_client)
        elif repo in ['xl', 'xivlauncher']:
            pass


DEFAULT_META = {
    "Changelog": "",
    "Tags": [],
    "IsHide": False,
    "TestingAssemblyVersion": None,
    "AcceptsFeedback": True,
    "FeedbackMessage": None,
    "FeedbackWebhook": None,
}

def regen_pluginmaster(redis_client = None, repo_url: str = ''):
    settings = get_settings()
    if not redis_client:
        redis_client = Redis.create_client()
    if not repo_url:
        repo_url = settings.plugin_repo
    repo_name = re.search(r'\/(?P<name>.*)\.git', repo_url).group('name')
    (_, repo) = update_git_repo(repo_url)
    branch = repo.active_branch.name
    plugin_namespace = f"plugin-{repo_name}-{branch}"
    plugin_repo_dir = get_repo_dir(repo_url)
    cahnnel_map = {
        'stable': 'stable',
        'testing': 'testing-live'
    }
    api_level = settings.plugin_api_level
    if repo_name == 'DalamudPlugins':  # old plugin dist repo
        cahnnel_map = {
            'stable': 'plugins',
            'testing': 'testing'
        }
        api_level = 6
    pluginmaster = []
    stable_dir = os.path.join(plugin_repo_dir, cahnnel_map['stable'])
    testing_dir = os.path.join(plugin_repo_dir, cahnnel_map['testing'])
    jsonc = JsonComment(json)
    for plugin_dir in [stable_dir, testing_dir]:
        for plugin in os.listdir(plugin_dir):
            try:
                with codecs.open(os.path.join(plugin_dir, f'{plugin}/{plugin}.json'), 'r', 'utf8') as f:
                    plugin_meta = jsonc.load(f)
            except FileNotFoundError:
                print(f"Cannot find plugin meta file for {plugin}")
                continue
            except json.decoder.JSONDecodeError:
                try:
                    with codecs.open(os.path.join(plugin_dir, f'{plugin}/{plugin}.json'), 'r', 'utf-8-sig') as f:
                        plugin_meta = jsonc.load(f)
                except Exception as e:
                    print(f"Cannot parse plugin meta file for {plugin}")
                    continue
            except Exception as e:
                print(f"Cannot parse plugin meta file for {plugin}")
                continue
            for key, value in DEFAULT_META.items():
                if key not in plugin_meta:
                    plugin_meta[key] = value
            is_testing = plugin_dir == testing_dir
            plugin_meta["IsTestingExclusive"] = is_testing
            if is_testing:
                plugin_meta["TestingAssemblyVersion"] = plugin_meta["AssemblyVersion"]
            plugin_meta["DalamudApiLevel"] = api_level
            plugin_meta["DownloadCount"] = 0  # TODO
            plugin_meta["LastUpdate"] = 0  # TODO
            plugin_meta["CategoryTags"] = []  # TODO
            plugin_meta["DownloadLinkInstall"] = settings.hosted_url.rstrip('/') \
                + '/Plugin/Download/' + f"{plugin}?isUpdate=False&isTesting=False&branch=api{api_level}"
            plugin_meta["DownloadLinkUpdate"] = settings.hosted_url.rstrip('/') \
                + '/Plugin/Download/' + f"{plugin}?isUpdate=True&isTesting=False&branch=api{api_level}"
            plugin_meta["DownloadLinkTesting"] = settings.hosted_url.rstrip('/') \
                + '/Plugin/Download/' + f"{plugin}?isUpdate=False&isTesting=True&branch=api{api_level}"
            plugin_latest_path = os.path.join(plugin_dir, f'{plugin}/latest.zip')
            (hashed_name, _) = cache_file(plugin_latest_path)
            plugin_name = f"{plugin}-testing" if is_testing else plugin
            redis_client.hset(f'xlweb-fastapi|{plugin_namespace}', plugin_name, hashed_name)
            pluginmaster.append(plugin_meta)
    redis_client.hset(f'xlweb-fastapi|{plugin_namespace}', 'pluginmaster', json.dumps(pluginmaster))
    print(f"Regenerated Pluginmaster for {plugin_namespace}: \n" + str(json.dumps(pluginmaster, indent=2)))
    return pluginmaster


def regen_asset(redis_client = None):
    if not redis_client:
        redis_client = Redis.create_client()
    settings = get_settings()
    update_git_repo(settings.asset_repo)
    asset_repo_dir = get_repo_dir(settings.asset_repo)
    with codecs.open(os.path.join(asset_repo_dir, "asset.json"), "r") as f:
        asset_json = json.load(f)
    asset_list = []
    for asset in asset_json["Assets"]:
        file_path = os.path.join(asset_repo_dir, asset["FileName"])
        (hashed_name, _) = cache_file(file_path)
        if "github" in asset["Url"]:  # only replace the github urls
            asset["Url"] = settings.hosted_url.rstrip('/') + '/File/Get/' + hashed_name
        asset_list.append(asset)
    asset_json["Assets"] = asset_list
    print("Regenerated Assets: \n" + str(json.dumps(asset_json, indent=2)))
    redis_client.hset('xlweb-fastapi|asset', 'meta', json.dumps(asset_json))
    return asset_json


def regen_dalamud(redis_client = None):
    if not redis_client:
        redis_client = Redis.create_client()
    settings = get_settings()
    update_git_repo(settings.dalamud_repo)
    dalamud_repo_dir = get_repo_dir(settings.dalamud_repo)
    runtime_verlist = []
    release_version = {}
    for track in ["release", "stg", "canary"]:
        dist_dir = dalamud_repo_dir if track == "release" else \
            os.path.join(dalamud_repo_dir, track)
        with codecs.open(os.path.join(dist_dir, 'version'), 'r', 'utf8') as f:
            version_json = json.load(f)
        if version_json['RuntimeRequired'] and version_json['RuntimeVersion'] not in runtime_verlist:
            runtime_verlist.append(version_json['RuntimeVersion'])
        ext_format = settings.dalamud_format  # zip or 7z
        dalamud_path = os.path.join(dist_dir, f"latest.{ext_format}")
        (hashed_name, _) = cache_file(dalamud_path)
        version_json['downloadUrl'] = settings.hosted_url.rstrip('/') + f'/File/Get/{hashed_name}'
        version_json['track'] = track
        if track == 'release':
            version_json['changelog'] = []
        if 'key' not in version_json:
            version_json['key'] = None
        redis_client.hset('xlweb-fastapi|dalamud', f'dist-{track}', json.dumps(version_json))
        if track == 'release':
            release_version = version_json
    file_cache_dir = os.path.join(settings.root_path, settings.file_cache_dir)
    for version in runtime_verlist:
        desktop_url = f'https://dotnetcli.azureedge.net/dotnet/WindowsDesktop/{version}/windowsdesktop-runtime-{version}-win-x64.zip'
        (hashed_name, _) = cache_file(download_file(desktop_url, file_cache_dir))
        redis_client.hset('xlweb-fastapi|runtime', f'desktop-{version}', hashed_name)
        dotnet_url = f'https://dotnetcli.azureedge.net/dotnet/Runtime/{version}/dotnet-runtime-{version}-win-x64.zip'
        (hashed_name, _) = cache_file(download_file(dotnet_url, file_cache_dir))
        redis_client.hset('xlweb-fastapi|runtime', f'dotnet-{version}', hashed_name)
    for hash_file in os.listdir(os.path.join(dalamud_repo_dir, 'runtimehashes')):
        version = re.search(r'(?P<ver>.*)\.json$', hash_file).group('ver')
        (hashed_name, _) = cache_file(os.path.join(dalamud_repo_dir, f'runtimehashes/{hash_file}'))
        redis_client.hset('xlweb-fastapi|runtime', f'hashes-{version}', hashed_name)
    return release_version

