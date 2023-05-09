import base64
import hashlib
import hmac
import json
import time
import requests
from typing import List
from . import CDN

class CTCDN(CDN):
    def __init__(self):
        self.name = 'CTCDN'
        self.ak = self.config.ctcdn_ak
        self.sk = self.config.ctcdn_sk
        self.ac = 'app'
        self.api_root = 'open.ctcdn.cn'

    @staticmethod
    def get_zone_name(url: str):
        zone_name = url
        prefix_removal = ['http://', 'https://']
        for rem in prefix_removal:
            if zone_name.startswith(rem):
                zone_name = zone_name[len(rem):]
        zone_name = zone_name.split('/')[0]
        return zone_name


    def purge_urls(self, urls: List[str]):
        self.refresh(1, urls)


    def _encode(self, key, content):
        """
        sha(secure hash algorithm)
        :param key: 用来加密的key
        :param content: 需要加密的数据
        :return: 密文
        """
        h = hmac.new(
            # base64安全加密，对齐位数
            base64.urlsafe_b64decode(key + "==="),
            content.encode(),
            hashlib.sha256
        )
        signature = base64.urlsafe_b64encode(h.digest()).decode().replace("=", "")
        return signature

    def _do_get(self, path):
        """
        构造请求体，发送请求
        注意：uri里必须包含请求参数
        :return:
        """
        # 当前时间戳，单位毫秒
        now = str(int(round(time.time() * 1000)))
        sign_str = self.ak + "\n" + now + "\n" + path
        t_now = int(int(now) / 86400000)
        # 首次encode
        tem_signature = self._encode(self.sk, self.ak + ":" + str(t_now))
        # 再次encode
        signature = self._encode(tem_signature, sign_str)
        # 固定的请求头部
        headers = {
            "x-alogic-now": now,
            "x-alogic-app": self.ak,
            "x-alogic-signature": signature,
            "x-alogic-ac": self.ac
        }
        url = "https://{}{}".format(self.api_root, path)
        response = requests.get(url, headers=headers, verify=False)
        msg = response.json()["message"]
        if msg == 'success':
            return (msg, 'info')
        else:
            return (msg, 'error')

    def _do_post(self, path, params):
        """
        构造请求体，发送请求
        :return:
        """
        # 当前时间戳，单位毫秒
        now = str(int(round(time.time() * 1000)))
        sign_str = self.ak + "\n" + now + "\n" + path
        t_now = int(int(now) / 86400000)
        # 首次encode
        tem_signature = self._encode(self.sk, self.ak + ":" + str(t_now))
        # 再次encode
        signature = self._encode(tem_signature, sign_str)
        # 固定的请求头部
        headers = {
            "x-alogic-now": now,
            "x-alogic-app": self.ak,
            "x-alogic-signature": signature,
            "x-alogic-ac": self.ac
        }
        url = "https://{}{}".format(self.api_root, path)
        response = requests.post(url, data=json.dumps(
            params), headers=headers, verify=False)
        msg = response.json()["message"]
        if msg == 'success':
            return (msg, 'message')
        else:
            return (msg, 'error')
    
    def refresh(self, type: int, urls: list):
        """刷新任务创建
        Args:
            type (int): 刷新类型，必须,类型说明: 1. url2. 目录dir 3.正则匹配re (数字类型)
            urls (list): 刷新参数值，必须，数组格式；刷新类型为url时单次最多1000条，类型为dir和re时单次最多50条。 (数组类型)
        """
        path = "/v1/refreshmanage/create"
        params = {
            "values": urls,
            "task_type": type
        }
        return self._do_post(path, params)


    def preload(self, urls: list):
        """预取任务创建
        Args:
            urls (list): 预取文件列表，数组格式，单次最多50条。如域名有做防盗链配置，则相应的预取url需同样带有防盗链。 (数组类型)
        """
        path = "/v1/preloadmanage/create"
        params = {
            "values": urls,
        }
        return self._do_post(path, params)


    def flow_packet(self):
        """剩余流量包查询
        """
        path = "/v1/order/flow-packet"
        params = ""

        return self._do_get(path)


    def top_url(self):
        path = "/v1/top_url"
        hosted_url = self.config.hosted_url
        zone_name = CTCDN.get_zone_name(hosted_url)
        params = {
            "domain": [zone_name],
            "top_rank": 100,
            "start_time": int(time.time()) - 3600 * 24,
            "end_time": int(time.time())
        }
        return self._do_post(path, params)