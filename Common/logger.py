#!/usr/bin/env python
# -*- coding: utf-8 -*
__author__ = 'zhouguangming'

import os, sys
import logging, time
from settings import  InfoLevel

class logger(logging.Handler):
    def __init__(self, logfilename, tester=None):
        super(logger, self).__init__()
        logging.basicConfig(level = logging.DEBUG, \
                            format='[%(asctime)s]:[%(levelname)s]%(message)s', \
                            datefmt='%Y-%m-%d %H:%M:%S', \
                            filename=logfilename, \
                            filemode='a')
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('[%(levelname)-8s]:%(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)

    def Log(self, message, level=InfoLevel.INFO_Level):
        '''输出具体的日志信息，并注明日志类型'''
        #print levelInfo[level] + message.decode("utf-8")
        if level == InfoLevel.INFO_Level:
            logging.info(message)
        elif level == InfoLevel.WARNING_Level:
            logging.warning(message)
        elif level == InfoLevel.ERROR_Level:
            logging.error(message)
        #self.Object.AppendText(levelInfo[level] + message.decode("utf-8"))

# 获取执行脚本所在路径
def current_path():   
    path=os.path.realpath(sys.path[0])
    if os.path.isfile(path):    
        path=os.path.dirname(path)    
        return os.path.abspath(path)
    return path

# 获取执行脚本所在上一级路径
def getLogPath():
    return os.path.dirname(os.path.realpath(sys.path[0]))