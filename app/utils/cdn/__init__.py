import abc
import traceback
from typing import Union, List

from logs import logger
from ..common import get_settings

class CDN(metaclass=abc.ABCMeta):
    name = 'Unknown'
    config = get_settings()
    
    def path_to_url(self, path):
        if not path:
            raise RuntimeError(f'Path cannot be null.')
        if path.startswith('http'):
            return path
        if path[0] != '/':
            path = '/' + path
        url = self.config.hosted_url.rstrip('/') + path
        return url

    def purge(self, paths: Union[str, List[str]]):
        url_list = [self.path_to_url(paths)] if type(paths) is str else [
            self.path_to_url(x) for x in paths
        ]
        logger.info(f"Purging urls of {self}: {url_list}")
        try:
            self.purge_urls(url_list)
        except Exception as e:
            traceback.print_exc()
            logger.error("Purging failed.")
            raise e
        logger.info("Purging finished.")

    @abc.abstractmethod
    def purge_urls(self, url: List[str]):
        raise NotImplementedError

    def __str__(self):
        return f'{self.name}'
