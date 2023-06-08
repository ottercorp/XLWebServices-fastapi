# !/usr/bin/env python
# -*- coding: utf-8 -*-
# cython:language_level=3
# @Time    : 2023/6/7 15:38
# @File    : ottercloudcdn.py

import requests

from . import CDN


class OtterCloudCDN(CDN):
    def __init__(self):
        self.name = 'OtterCloudCDN'
        self.cdn_host = self.config.ottercloud_cdn_host
        self.id = self.config.ottercloud_cdn_id
        self.key = self.config.ottercloud_cdn_key

    @staticmethod
    def get_host_name(url: str):
        host_name = url
        prefix_removal = ['http://', 'https://']
        for rem in prefix_removal:
            if host_name.startswith(rem):
                host_name = host_name[len(rem):]
        host_name = host_name.split('/')[0]
        return host_name

    def _get_token(self):
        url = f'https://{self.cdn_host}/APIAccessTokenService/getAPIAccessToken'
        data = {
            "type": "admin",
            "accessKeyId": self.id,
            "accessKey": self.key
        }
        response = requests.post(url, json=data)
        if response.status_code != 200:
            raise RuntimeError(f'Cannot get token. {response.text}')
        return response.json()['data']['token']

    def _do_get(self, api_path):
        headers = {
            'X-Edge-Access-Token': self._get_token()
        }
        url = "https://{}{}".format(self.cdn_host, api_path)
        response = requests.get(url, headers=headers, verify=False)
        status_code = response.json()['code']
        msg = response.json()['message']
        if status_code == 200:
            return (msg, 'info')
        else:
            return (msg, 'error')

    def _do_post(self, api_path, params: dict):
        headers = {
            'X-Edge-Access-Token': self._get_token()
        }
        url = "https://{}{}".format(self.cdn_host, api_path)
        response = requests.post(url, headers=headers, json=params, verify=False)
        status_code = response.json()['code']
        msg = response.json()['message']
        if status_code == 200:
            return (msg, 'info')
        else:
            return (msg, 'error')

    def refresh(self, type: int, urls: list):
        """刷新任务创建
        Args:
            type (int): 刷新类型，必须,类型说明: 1. url 2. 目录dir
            urls (list): 刷新参数值，必须，数组格式；刷新类型为url时单次最多1000条，类型为dir和re时单次最多50条。 (数组类型)
        """
        path = "/HTTPCacheTaskService/createHTTPCacheTask"
        if type == 1:
            type_str = "key"
        elif type == 2:
            type_str = "prefix"
        else:
            raise ValueError(f'Unknown type {type}')
        params = {
            "type": "purge",
            "keyType": type_str,
            "keys": urls,
        }
        return self._do_post(path, params)

    def purge_urls(self, urls: list[str]):
        self.refresh(1, urls)
