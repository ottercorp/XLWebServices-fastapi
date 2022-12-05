import os
import json
import tempfile
import codecs
from typing import Union, List
from .common import get_settings
from crowdin_api import CrowdinClient
from crowdin_api import exceptions as crowdin_exceptions
from .redis import Redis

class Crowdin():
    config = get_settings()
    
    def __init__(self):
        self.client = CrowdinClient(token=self.config.crowdin_token)
        projects = self.client.projects.list_projects()
        for proj in projects['data']:
            if proj['data']['name'] == self.config.crowdin_project_name:
                 self.proj = proj
                 self.proj_id = proj['data']['id']
                 break


    def update_redis(self, pluginmaster: list):
        r = Redis.create_client()
        desc_str = r.hget(f'{self.config.redis_prefix}crowdin', 'plugin-description') or '{}'
        desc_json = json.loads(desc_str)
        punchline_str = r.hget(f'{self.config.redis_prefix}crowdin', 'plugin-punchline') or '{}'
        punchline_json = json.loads(punchline_str)
        for plugin in pluginmaster:
            desc_json.update({
                plugin['InternalName']: plugin['Description']
            })
            punchline_json.update({
                plugin['InternalName']: plugin['Punchline']
            })
        r.hset(f'{self.config.redis_prefix}crowdin', 'plugin-description', json.dumps(desc_json))
        r.hset(f'{self.config.redis_prefix}crowdin', 'plugin-punchline', json.dumps(punchline_json))


    def upload_resource(self, resource_name: str, resource_content: str):
        with tempfile.TemporaryDirectory() as tmp:
            file_path = os.path.join(tmp, resource_name)
            with open(file_path, 'w') as f:
                f.write(resource_content)
            with open(file_path, 'r') as f:
                storage = self.client.storages.add_storage(f)
        files = self.client.source_files.list_files(self.proj_id)
        file_id = None
        for file in files['data']:
            if file['data']['name'] == resource_name:
                file_id = file['data']['id']
                break
        if file_id:
            return self.client.source_files.update_file(self.proj_id, file_id, storage['data']['id'])
        return self.client.source_files.add_file(self.proj_id, storage['data']['id'], resource_name)


    def upload_resources(self):
        r = Redis.create_client()
        desc_str = r.hget(f'{self.config.redis_prefix}crowdin', 'plugin-description') or '{}'
        punchline_str = r.hget(f'{self.config.redis_prefix}crowdin', 'plugin-punchline') or '{}'
        desc_file = self.upload_resource('description.json', desc_str)
        punchline_file = self.upload_resource('punchline.json', punchline_str)


    def load_translations(self):
        r = Redis.create_client()
        lang = self.config.default_pm_lang
        root_path = self.config.root_path
        loc_folder = os.path.join(root_path, f'translations/{lang}')
        if not os.path.exists(loc_folder) or not os.path.isdir(loc_folder):
            return
        if lang == 'en-US':
            return
        desc_path = os.path.join(loc_folder, 'description.json')
        with codecs.open(desc_path, 'r', 'utf8') as f:
            desc = json.load(f)
        punchline_path = os.path.join(loc_folder, 'punchline.json')
        with codecs.open(punchline_path, 'r', 'utf8') as f:
            punchline = json.load(f)
        r.hset(f'{self.config.redis_prefix}crowdin', f'plugin-description-{lang}', json.dumps(desc))
        r.hset(f'{self.config.redis_prefix}crowdin', f'plugin-punchline-{lang}', json.dumps(punchline))
