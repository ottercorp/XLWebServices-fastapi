import CloudFlare
from . import CDN
from typing import List

class CloudFlareCDN(CDN):
    def __init__(self):
        self.name = 'CloudFlare'
        self.cf = CloudFlare.CloudFlare(token=self.config.cf_token)
        self.client = self.cf


    @staticmethod
    def get_host_name(url: str):
        host_name = url
        prefix_removal = ['http://', 'https://']
        for rem in prefix_removal:
            if host_name.startswith(rem):
                host_name = host_name[len(rem):]
        host_name = host_name.split('/')[0]
        return host_name

    
    def get_zone_id(self, url: str):
        if self.config.cf_zone_id:
            return self.config.cf_zone_id
        host_name = CloudFlareCDN.get_host_name(url)
        zones = self.client.zones.get(params = {'per_page':100})
        if not zones:
            raise RuntimeError('Cannot get zones.')
        for zone in zones:
            if zone['name'] in host_name:
                return zone['id']
        raise RuntimeError(f'Cannot get zone name for \"{host_name}\".')


    def purge_urls(self, urls: List[str]):
        zone_id = self.get_zone_id(urls[0])
        self.client.zones.purge_cache.post(zone_id, data={'files':urls})
