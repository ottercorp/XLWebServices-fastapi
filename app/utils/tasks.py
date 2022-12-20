import logging
import os
import re
import json
import shutil
import redis
import codecs
import hashlib
import toml
import concurrent.futures
import commentjson
from collections import defaultdict
from itertools import product
from typing import Union, Tuple
from .common import get_settings, cache_file, download_file
from .git import update_git_repo, get_repo_dir, get_user_repo_name
from .redis import Redis
from .cdn.cloudflare import CloudFlareCDN
from .cdn.ctcdn import CTCDN
from github import Github
from termcolor import colored

from logs import logger


def regen(task_list: list[str]):
    settings = get_settings()

    logger.info(f"Started regeneration tasks: {task_list}.")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(regen_task, task_list)
        results_str = ""
        for (task, result) in zip(task_list, results):
            ok = colored("ok", "green") if result else colored("failed", "red")
            results_str += f"{task}: {ok}\n"
        logger.info(f"Regeneration tasks finished with results: {results_str.strip()}")

    cdn_client_list = []
    for cdn in settings.cdn_list:
        if cdn == 'cloudflare':
            cdn_client_list.append(CloudFlareCDN())
        elif cdn == 'ctcdn':
            cdn_client_list.append(CTCDN())
    task_cdn_list = list(product(task_list, cdn_client_list))

    logger.info(f"Started CDN refresh tasks: {task_cdn_list}.")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(refresh_cdn_task, task_cdn_list)
        results_str = ""
        for (task_cdn, result) in zip(task_cdn_list, results):
            task, cdn = task_cdn
            ok = colored("ok", "green") if result else colored("failed", "red")
            results_str += f"{task}-{cdn}: {ok}\n"
        logger.info(f"CDN refresh tasks finished with results: {results_str.strip()}")

def regen_task(task: str):
    logger.info(f"Started regeneration task: {task}.")
    try:
        redis_client = Redis.create_client()
        task_map = {
            'dalamud': regen_dalamud,
            'dalamud_changelog': regen_dalamud_changelog,
            'plugin': regen_pluginmaster,
            'asset': regen_asset,
            'xl': regen_xivlauncher,
            'xivl': regen_xivlauncher,
            'xivlauncher': regen_xivlauncher,
        }
        if task in task_map:
            func = task_map[task]
            func(redis_client)
        else:
            raise RuntimeError("Invalid task")
        logger.info(f"Regeneration task {task} finished.")
        return True
    except Exception as e:
        logger.error(e)
        logger.error(f"Regeneration task {task} failed.")
        return False


def refresh_cdn_task(task_cdn: Tuple[str, Union[CloudFlareCDN, CTCDN]]):
    task, cdn = task_cdn
    logger.info(f"Started CDN refresh task: {cdn}-{task}.")
    try:
        settings = get_settings()
        path_map = {
            'dalamud': ['/Dalamud/Release/VersionInfo', '/Dalamud/Release/Meta'] + \
                [f'/Release/VersionInfo?track={x}' for x in ['release', 'staging', 'stg', 'canary']],
            'dalamud_changelog': ['/Plugin/CoreChangelog'],
            'plugin': ['/Plugin/PluginMaster'],
            'asset': ['/Dalamud/Asset/Meta'],
            'xl': ['/Proxy/Meta'],
            'xivl': ['/Proxy/Meta'],
            'xivlauncher': ['/Proxy/Meta'],
        }
        if task in path_map:
            cdn.purge(path_map[task])
        else:
            raise RuntimeError("Invalid task")
        logger.info(f"CDN refresh task {cdn}-{task} finished.")
        return True
    except Exception as e:
        logger.error(e)
        logger.error(f"CDN refresh task {cdn}-{task} failed.")
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
    logger.info("Start regenerating pluginmaster.")
    settings = get_settings()
    if not redis_client:
        redis_client = Redis.create_client()
    if not repo_url:
        repo_url = settings.plugin_repo
    is_dip17 = True  # default to be using dip17
    (_, repo_name) = get_user_repo_name(repo_url)
    (_, repo) = update_git_repo(repo_url)
    branch = repo.active_branch.name
    plugin_namespace = f"plugin-{repo_name}-{branch}"
    logger.info(f"plugin_namespace: {plugin_namespace}")
    plugin_repo_dir = get_repo_dir(repo_url)
    cahnnel_map = {
        'stable': 'stable',
        'testing': 'testing-live'
    }
    if repo_name == 'DalamudPlugins':  # old plugin dist repo
        cahnnel_map = {
            'stable': 'plugins',
            'testing': 'testing'
        }
        is_dip17 = False
    pluginmaster = []
    stable_dir = os.path.join(plugin_repo_dir, cahnnel_map['stable'])
    testing_dir = os.path.join(plugin_repo_dir, cahnnel_map['testing'])
    jsonc = commentjson
    # Load categories
    category_tags = defaultdict(list)
    category_path = os.path.join(settings.root_path, 'app/utils/categoryfallbacks.json')
    if os.path.exists(category_path):
        with codecs.open(category_path, "r", "utf8") as f:
            category_tags.update(jsonc.load(f))
    # Load last update time
    last_updated = {}
    if not is_dip17:
        legacy_pluginmaster = []
        legacy_pluginmaster_path = os.path.join(plugin_repo_dir, 'pluginmaster.json')
        with codecs.open(legacy_pluginmaster_path, 'r', 'utf8') as f:
            legacy_pluginmaster = jsonc.load(f)
        for legacy_meta in legacy_pluginmaster:
            last_updated[legacy_meta['InternalName']] = int(legacy_meta['LastUpdated'])
    else:
        state_path = os.path.join(plugin_repo_dir, 'State.toml')
        with codecs.open(state_path, 'r', 'utf8') as f:
            state = toml.load(f)
        for (channel, channel_meta) in state['channels'].items():
            for (plugin, plugin_meta) in channel_meta['plugins'].items():
                last_updated[plugin] = int(plugin_meta['time_built'].timestamp())
    # Generate pluginmaster
    for plugin_dir in [stable_dir, testing_dir]:
        for plugin in os.listdir(plugin_dir):
            try:
                with codecs.open(os.path.join(plugin_dir, f'{plugin}/{plugin}.json'), 'r', 'utf8') as f:
                    plugin_meta = jsonc.load(f)
            except FileNotFoundError:
                logger.error(f"Cannot find plugin meta file for {plugin}")
                continue
            except Exception as e:
                try:
                    with codecs.open(os.path.join(plugin_dir, f'{plugin}/{plugin}.json'), 'r', 'utf-8-sig') as f:
                        plugin_meta = jsonc.load(f)
                except Exception as e:
                    logger.error(f"Cannot parse plugin meta file for {plugin}")
                    continue
            for key, value in DEFAULT_META.items():
                if key not in plugin_meta:
                    plugin_meta[key] = value
            is_testing = plugin_dir == testing_dir
            plugin_meta["IsTestingExclusive"] = is_testing
            if is_testing:
                plugin_meta["TestingAssemblyVersion"] = plugin_meta["AssemblyVersion"]
            api_level = int(plugin_meta.get("DalamudApiLevel", 0))
            download_count = redis_client.hget(f'{settings.redis_prefix}plugin-count', plugin) or 0
            plugin_meta["DownloadCount"] = int(download_count)
            plugin_meta["LastUpdate"] = last_updated.get(plugin, plugin_meta.get("LastUpdate", 0))
            plugin_meta["CategoryTags"] = category_tags[plugin]
            plugin_meta["DownloadLinkInstall"] = settings.hosted_url.rstrip('/') \
                + '/Plugin/Download/' + f"{plugin}?isUpdate=False&isTesting=False&branch=api{api_level}"
            plugin_meta["DownloadLinkUpdate"] = settings.hosted_url.rstrip('/') \
                + '/Plugin/Download/' + f"{plugin}?isUpdate=True&isTesting=False&branch=api{api_level}"
            plugin_meta["DownloadLinkTesting"] = settings.hosted_url.rstrip('/') \
                + '/Plugin/Download/' + f"{plugin}?isUpdate=False&isTesting=True&branch=api{api_level}"
            plugin_latest_path = os.path.join(plugin_dir, f'{plugin}/latest.zip')
            (hashed_name, _) = cache_file(plugin_latest_path)
            plugin_name = f"{plugin}-testing" if is_testing else plugin
            redis_client.hset(f'{settings.redis_prefix}{plugin_namespace}', plugin_name, hashed_name)
            pluginmaster.append(plugin_meta)
    redis_client.hset(f'{settings.redis_prefix}{plugin_namespace}', 'pluginmaster', json.dumps(pluginmaster))
    # print(f"Regenerated Pluginmaster for {plugin_namespace}: \n" + str(json.dumps(pluginmaster, indent=2)))


def regen_asset(redis_client = None):
    logger.info("Start regenerating dalamud assets.")
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
    # print("Regenerated Assets: \n" + str(json.dumps(asset_json, indent=2)))
    redis_client.hset(f'{settings.redis_prefix}asset', 'meta', json.dumps(asset_json))


def regen_dalamud(redis_client = None):
    logger.info("Start regenerating dalamud distribution.")
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
        if 'key' not in version_json and 'Key' not in version_json:
            version_json['key'] = None
        redis_client.hset(f'{settings.redis_prefix}dalamud', f'dist-{track}', json.dumps(version_json))
        if track == 'release':
            release_version = version_json
    for version in runtime_verlist:
        desktop_url = f'https://dotnetcli.azureedge.net/dotnet/WindowsDesktop/{version}/windowsdesktop-runtime-{version}-win-x64.zip'
        (hashed_name, _) = cache_file(download_file(desktop_url))
        redis_client.hset(f'{settings.redis_prefix}runtime', f'desktop-{version}', hashed_name)
        dotnet_url = f'https://dotnetcli.azureedge.net/dotnet/Runtime/{version}/dotnet-runtime-{version}-win-x64.zip'
        (hashed_name, _) = cache_file(download_file(dotnet_url))
        redis_client.hset(f'{settings.redis_prefix}runtime', f'dotnet-{version}', hashed_name)
    for hash_file in os.listdir(os.path.join(distrib_repo_dir, 'runtimehashes')):
        version = re.search(r'(?P<ver>.*)\.json$', hash_file).group('ver')
        (hashed_name, _) = cache_file(os.path.join(distrib_repo_dir, f'runtimehashes/{hash_file}'))
        redis_client.hset(f'{settings.redis_prefix}runtime', f'hashes-{version}', hashed_name)
    # return release_version


def regen_dalamud_changelog(redis_client = None):
    logger.info("Start regenerating dalamud changelog.")
    if not redis_client:
        redis_client = Redis.create_client()
    settings = get_settings()
    dalamud_repo_url = settings.dalamud_repo
    user, repo_name = get_user_repo_name(dalamud_repo_url)
    gh = Github(None if not settings.github_token else settings.github_token)
    repo = gh.get_repo(f'{user}/{repo_name}')
    tags = repo.get_tags()
    sliced_tags = list(tags[:11]) # only care about latest 10 tags
    changelogs = []
    skip_prefix = ['build:', 'Merge pull request', 'Merge branch']
    for (idx, tag) in enumerate(sliced_tags[:-1]):
        next_tag = sliced_tags[idx + 1]
        changes = []
        diff = repo.compare(next_tag.commit.sha, tag.commit.sha)
        for commit in diff.commits:
            msg = commit.commit.message
            if any([msg.startswith(x) for x in skip_prefix]):
                continue
            changes.append({
                'author': commit.commit.author.name,
                'message': msg.split('\n')[0],
                'sha': commit.sha,
                'date': commit.commit.author.date.isoformat()
            })
        changelogs.append({
            'version': tag.name,
            'date': tag.commit.commit.author.date.isoformat(),
            'changes': changes,
        })
    redis_client.hset(f'{settings.redis_prefix}dalamud', 'changelog', json.dumps(changelogs))


def regen_xivlauncher(redis_client = None):
    logger.info("Start regenerating xivlauncher distribution.")
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
        redis_client.hset(f'{settings.redis_prefix}xivlauncher', f'{release_type}-tag', rel.tag_name)
        changelog = ''
        for asset in rel.get_assets():
            asset_filepath = download_file(asset.browser_download_url, force=True)  # overwrite file
            if asset.name == 'RELEASES':
                with codecs.open(asset_filepath, 'r', 'utf8') as f:
                    releases_list = f.read()
                redis_client.hset(f'{settings.redis_prefix}xivlauncher', f'{release_type}-releaseslist', releases_list)
                continue
            if asset.name == 'CHANGELOG.txt':
                with codecs.open(asset_filepath, 'r', 'utf8') as f:
                    changelog = f.read()
            (hashed_name, _) = cache_file(asset_filepath)
            redis_client.hset(
                f'{settings.redis_prefix}xivlauncher',
                f'{release_type}-{asset.name}',
                hashed_name
            )
        track = release_type.capitalize()
        meta = {
            'releasesInfo': f"/Proxy/Update/{track}/RELEASES",
            'version': rel.tag_name,
            'url': rel.html_url,
            'changelog': changelog,
            'when': rel.published_at.isoformat(),
        }
        redis_client.hset(
            f'{settings.redis_prefix}xivlauncher',
            f'{release_type}-meta',
            json.dumps(meta)
        )
