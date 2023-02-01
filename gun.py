# !/usr/bin/env python
# -*- coding: utf-8 -*-
# cython:language_level=3
# @Time    : 2022/8/20 23:22
# @Author  : subjadeites
# @File    : gun.py

import multiprocessing

debug = False
loglevel = 'info'
bind = '0.0.0.0:8080'
pidfile = 'logs/gunicorn.pid'
logfile = 'logs/debug.log'
errorlog = './logs/error.log'

# 启动的进程数
workers = multiprocessing.cpu_count()
worker_class = 'uvicorn.workers.UvicornH11Worker'
preload_app = True

x_forwarded_for_header = 'X-FORWARDED-FOR'
