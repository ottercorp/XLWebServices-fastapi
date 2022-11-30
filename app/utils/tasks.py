import os
import re
import json
import shutil
import redis
import codecs
import hashlib
import asyncio
from .common import get_settings, cache_file, download_file
from .git import update_git_repo, get_repo_dir
from .redis import Redis
from github import Github
from jsoncomment import JsonComment


async def regen(task_list: list[str]):
    print(f"Started regeneration tasks: {task_list}.")
    results = await asyncio.gather(
        *map(regen_task, task_list)
    )
    print(f"Regeneration tasks finished with results:\n{results}.")

async def regen_task(task: str):
    print(f"Started regeneration task: {task}.")
    try:
        redis_client = Redis.create_client()
        if task == 'dalamud':
            regen_dalamud(redis_client)
        elif task == 'plugin':
            regen_pluginmaster(redis_client)
        elif task == 'asset':
            regen_asset(redis_client)
        elif task in ['xl', 'xivlauncher']:
            regen_xivlauncher(redis_client)
        else:
            raise RuntimeError("Invalid task")
        print(f"Regeneration task {task} finished.")
        return True
    except Exception as e:
        print(e)
        print(f"Regeneration task {task} failed.")
        return False



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
    print("Start regenerating pluginmaster.")
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
    print("Start regenerating dalamud assets.")
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
    print("Start regenerating dalamud distribution.")
    if not redis_client:
        redis_client = Redis.create_client()
    settings = get_settings()
    update_git_repo(settings.distrib_repo)
    distrib_repo_dir = get_repo_dir(settings.distrib_repo)
    runtime_verlist = []
    release_version = {}
    for track in ["release", "stg", "canary"]:
        dist_dir = distrib_repo_dir if track == "release" else \
            os.path.join(distrib_repo_dir, track)
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
    for version in runtime_verlist:
        desktop_url = f'https://dotnetcli.azureedge.net/dotnet/WindowsDesktop/{version}/windowsdesktop-runtime-{version}-win-x64.zip'
        (hashed_name, _) = cache_file(download_file(desktop_url))
        redis_client.hset('xlweb-fastapi|runtime', f'desktop-{version}', hashed_name)
        dotnet_url = f'https://dotnetcli.azureedge.net/dotnet/Runtime/{version}/dotnet-runtime-{version}-win-x64.zip'
        (hashed_name, _) = cache_file(download_file(dotnet_url))
        redis_client.hset('xlweb-fastapi|runtime', f'dotnet-{version}', hashed_name)
    for hash_file in os.listdir(os.path.join(distrib_repo_dir, 'runtimehashes')):
        version = re.search(r'(?P<ver>.*)\.json$', hash_file).group('ver')
        (hashed_name, _) = cache_file(os.path.join(distrib_repo_dir, f'runtimehashes/{hash_file}'))
        redis_client.hset('xlweb-fastapi|runtime', f'hashes-{version}', hashed_name)
    return release_version


def regen_xivlauncher(redis_client = None):
    print("Start regenerating xivlauncher distribution.")
    if not redis_client:
        redis_client = Redis.create_client()
    settings = get_settings()
    xivl_repo_url = settings.xivl_repo
    s = re.search(r'github.com[\/:](?P<user>.+)\/(?P<repo>.+)\.git', xivl_repo_url)
    user, repo_name = s.group('user'), s.group('repo')
    gh = Github(None if not settings.github_token else settings.github_token)
    repo = gh.get_repo(f'{user}/{repo_name}')
    releases = repo.get_releases()
    pre_release = None
    release = None
    latest_release = releases[0]
    if latest_release.prerelease:
        pre_release = latest_release
        for r in releases:
            if not r.prerelease:
                release = r
                break
    else:
        pre_release = release = latest_release

    for (idx, rel) in enumerate([pre_release, release]):
        release_type = 'prerelease' if idx == 0 else 'release'
        redis_client.hset('xlweb-fastapi|xivlauncher', f'{release_type}-tag', rel.tag_name)
        changelog = ''
        for asset in rel.get_assets():
            asset_filepath = download_file(asset.browser_download_url, force=True)  # overwrite file
            if asset.name == 'RELEASES':
                with codecs.open(asset_filepath, 'r', 'utf8') as f:
                    releases_list = f.read()
                redis_client.hset('xlweb-fastapi|xivlauncher', f'{release_type}-releaseslist', releases_list)
                continue
            if asset.name == 'CHANGELOG.txt':
                with codecs.open(asset_filepath, 'r', 'utf8') as f:
                    changelog = f.read()
            (hashed_name, _) = cache_file(asset_filepath)
            redis_client.hset(
                'xlweb-fastapi|xivlauncher',
                f'{release_type}-{asset.name}',
                hashed_name
            )
        track = release_type.capitalize()
        meta = {
            'ReleasesInfo': f"/Proxy/Update/{track}/RELEASES",
            'Version': rel.tag_name,
            'Url': rel.html_url,
            'Changelog': changelog,
            'When': rel.published_at.isoformat(),
        }
        redis_client.hset(
            'xlweb-fastapi|xivlauncher',
            f'{release_type}-meta',
            json.dumps(meta)
        )
