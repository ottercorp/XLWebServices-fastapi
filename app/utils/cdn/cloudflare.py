import CloudFlare
from . import CDN
from typing import List

class CloudFlareCDN(CDN):
    def __init__(self):
        self.name = 'CloudFlare'
        self.cf = CloudFlare.CloudFlare(token=self.config.cf_token)
        self.client = self.cf


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
        zone_name = CloudFlareCDN.get_zone_name(urls[0])
        if self.config.cf_host_overwrite:
            zone_name = self.config.cf_host_overwrite
        zones = self.client.zones.get(params = {'name':zone_name,'per_page':100})
        if not zones:
            raise RuntimeError(f'Cannot get zone name: {zone_name}')
        zone = zones[0]
        self.client.zones.purge_cache.post(zone['id'], data={'files':urls})
