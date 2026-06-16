import codecs
import hashlib
import os
import re
import shutil
from functools import cache
from urllib.parse import unquote, urlparse

import requests

from logs import logger
from ..config import Settings


DOWNLOAD_HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/126.0.0.0 Safari/537.36'
    ),
}


@cache
def get_settings():
    return Settings()


@cache
def get_apilevel_namespace_map():
    return get_settings().api_namespace


@cache
def get_namespace_apilevel_map():
    return dict([(v, k) for (k, v) in get_settings().api_namespace.items()])


@cache
def get_tos_content():
    tos_path = os.path.join(get_settings().root_path, "ToS")
    with codecs.open(tos_path, "r", "utf8") as f:
        tos_content = f.read()
    return tos_content


@cache
def get_tos_hash():
    tos_content = get_tos_content()
    tos_hash = hashlib.sha256(tos_content.encode()).hexdigest()
    return tos_hash


def cache_file(file_path: str):
    settings = get_settings()
    file_cache_dir = os.path.join(settings.root_path, settings.file_cache_dir)
    if not os.path.exists(file_cache_dir):
        os.makedirs(file_cache_dir, exist_ok=True)
    try:
        with open(file_path, "rb") as f:
            bs = f.read()
    except FileNotFoundError:
        logger.error("File not found: " + file_path)
        return None
    sha256_hash = hashlib.sha256(bs).hexdigest()
    s = re.search(r'(?P<name>[^/\\&\?]+)\.(?P<ext>\w+)', file_path)
    hashed_name = f"{s.group('name')}.{sha256_hash}.{s.group('ext')}"
    hashed_path = os.path.join(file_cache_dir, hashed_name)
    logger.info(f"Caching {file_path} -> {hashed_path}")
    shutil.copy(file_path, hashed_path)
    return hashed_name, hashed_path


def download_file(url, dst="", force: bool = False, filename: str = "", timeout: float = 60):
    settings = get_settings()
    file_cache_dir = os.path.join(settings.root_path, settings.file_cache_dir)
    if not dst:
        dst = file_cache_dir
    if not os.path.exists(dst):
        os.makedirs(dst, exist_ok=True)
    parsed_url = urlparse(url)
    local_filename = filename or unquote(os.path.basename(parsed_url.path))
    if not local_filename:
        raise RuntimeError(f"Cannot infer file name from url: {url}")
    filepath = os.path.join(dst, local_filename)
    if os.path.exists(filepath) and not force:
        logger.info(f"File {filepath} exists, skipping download")
        return filepath
    logger.info(f"Downloading {url} -> {filepath}")
    with requests.get(url, stream=True, timeout=timeout, headers=DOWNLOAD_HEADERS) as r:
        r.raise_for_status()
        with open(filepath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return filepath
