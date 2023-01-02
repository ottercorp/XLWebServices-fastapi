# !/usr/bin/env python
# -*- coding: utf-8 -*-
# cython:language_level=3
# @Time    : 2022/12/8 16:57
# @File    : logger.py


import logging
from logging.handlers import TimedRotatingFileHandler


class Logger:
    def __init__(self, path, Clevel: int = logging.DEBUG, Flevel: int = logging.DEBUG, handler="one_file"):
        """output log to file and console

        Args:
            path(str): /path/filename
            Clevel(int): Level of console output
            Flevel(int): Level of file output
            handler(str): default one_file, if you want to use [TimedRotatingFileHandler] , set handler=""
        Returns:
            None
        """
        logging.captureWarnings(True) # Capture warning messages
        self.logger = logging.getLogger(path)
        self.logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')

        # 设置CMD日志
        self.sh = logging.StreamHandler()
        self.sh.setFormatter(fmt)
        self.sh.setLevel(Clevel)
        # 设置文件日志
        if handler == "one_file":
            self.fh = logging.FileHandler(path, encoding='utf-8')
        else:
            self.fh = TimedRotatingFileHandler(path, when="midnight", interval=1, encoding='utf-8')
        self.fh.suffix = "%Y%m%d"
        self.fh.setFormatter(fmt)
        self.fh.setLevel(Flevel)
        self.logger.addHandler(self.sh)
        self.logger.addHandler(self.fh)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def cri(self, message):
        self.logger.critical(message)

    def set_level(self, clevel: int = logging.DEBUG, Flevel: int = logging.DEBUG):
        self.logger.setLevel(logging.DEBUG)
        self.sh.setLevel(clevel)
        self.fh.setLevel(Flevel)
        self.logger.addHandler(self.sh)
        self.logger.addHandler(self.fh)

    def exception(self, message):
        self.error("++++++++++++ERROR++++++++++++")
        self.error(repr(message))
        self.logger.exception(message)
        self.error("+++++++++++++++++++++++++++++")


# Instantiate the logger object, one log file per day, INFO level and above logs are output to the console, INFO level and above logs are output to the file
logger = Logger(path="logs/app.log", Clevel=logging.INFO, Flevel=logging.INFO, handler='')
