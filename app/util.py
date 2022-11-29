import os
import re
import json
import shutil
import redis
import codecs
import hashlib
import git
from .config import Settings
from functools import cache
from fastapi import Depends
from jsoncomment import JsonComment


@cache
def get_settings():
    return Settings()


def cache_file(file_path: str):
    settings = get_settings()
    file_cache_dir = os.path.join(settings.root_path, settings.file_cache_dir)
    try:
        with open(file_path,"rb") as f:
            bs = f.read()
    except FileNotFoundError:
        print("File not found: " + file_path)
        return None
    sha256_hash = hashlib.sha256(bs).hexdigest()
    s = re.search(r'(?P<name>[^/\\&\?]+)\.(?P<ext>\w+)', file_path)
    hashed_name = f"{s.group('name')}.{sha256_hash}.{s.group('ext')}"
    hashed_path = os.path.join(file_cache_dir, hashed_name)
    print(f"Caching {file_path} -> {hashed_path}")
    shutil.copy(file_path, hashed_path)
    return hashed_name, hashed_path



def get_git_hash(repo_path: str = '', short_sha: bool = True, check_dirty: bool = True):
    repo = git.Repo(repo_path)
    sha = repo.head.commit.hexsha
    if short_sha:
        sha = sha[:7]
    dirty = '-dirty' if repo.is_dirty() and check_dirty else ''
    return f'{sha}{dirty}'


def get_repo_dir(git_url: str):
    settings = get_settings()
    repo_name = re.search(r'\/(?P<name>.*)\.git', git_url).group('name')
    repo_root_dir = os.path.join(settings.root_path, settings.repo_cache_dir)
    repo_dir = os.path.join(repo_root_dir, repo_name)
    if not os.path.exists(repo_dir) or not os.path.isdir(repo_dir):
        os.mkdir(repo_dir)
    return repo_dir


def get_git_repo(git_url: str, shallow: bool = True):
    repo_dir = get_repo_dir(git_url)
    if os.path.exists(os.path.join(repo_dir, ".git")):
        return git.Repo(repo_dir)
    options = ['--depth=1'] if shallow else []
    return git.Repo.clone_from(
        git_url,
        repo_dir,
        multi_options=['--depth=1']
    )


def update_git_repo(git_url: str):
    repo = get_git_repo(git_url)
    pull = repo.remotes.origin.pull()
    info = pull[0]
    assert info.flags & info.ERROR == 0, f"Error while pulling repo {git_url}"
    assert info.flags & info.REJECTED == 0, f"Rejected while pulling repo {git_url}"
    return info, repo


class Redis():
    @staticmethod
    def create_client():
        settings = get_settings()
        return redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0, decode_responses=True)


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
    # "CategoryTags": [],
    "IsHide": False,
    "TestingAssemblyVersion": None,
    # "IsTestingExclusive": False,
    # "DalamudApiLevel": 0,
    # "DownloadCount": 0,
    # "LastUpdate": 0,
    # "DownloadLinkInstall": "",
    # "DownloadLinkUpdate": "",
    # "DownloadLinkTesting": "",
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
    

