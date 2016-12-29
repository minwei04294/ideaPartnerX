#!/usr/bin/env python
# -*- coding: utf-8 -*
__author__ = 'ZQ'

from Common.logger import logger
from Common.settings import *
from tactics_drivers.EditFastRegressionDriver import *
from Common.GetFiddlerData import *
from tactics_drivers.SmokeDriver import *
import sys

if __name__ == '__main__':
    Logger = logger(logfilename)

    dbid = sys.argv[1]
    userid = sys.argv[2]
    if sys.argv[3] == '1':
        #将fiddler抓包写入LOG_TEST.FIDDLER_BASE_DATA表
        zipdir = sys.argv[4]
        unzipdir = sys.argv[5]
        IBD = IniBaseData(LogTestDBConf, Logger, zipdir, unzipdir)
        IBD.run()
        #将FIDDLER_BASE_DATA表数据写入strategy_edit_fast_regression表
        ATD = analyzeTacticsData(LogTestDBConf, Logger)
        ATD.run()
    elif sys.argv[3] == '2':
        SR = SmokeRunner(dbid, userid, LogTestDBConf, Logger)
        c_idlist = sys.argv[4].decode('gbk').encode('utf-8').split(',')
        SR.run(c_idlist)
