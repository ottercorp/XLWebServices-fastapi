import os
import re
import json
import shutil
import redis
import codecs
import hashlib
import git
from ..config import Settings
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
