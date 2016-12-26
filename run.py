#!/usr/bin/env python
# -*- coding: utf-8 -*
# 用于数据数据编辑请求的挖掘驱动
__author__ = 'wangjun'

from Common.logger import logger
from Common.settings import *
from tactics_drivers.EditFastRegressionDriver import *
from Common.GetFiddlerData import *
from tactics_drivers.SmokeDriver import *
import sys

if __name__ == '__main__':
    Logger = logger(logfilename)

    dbid = 257
    userid = sys.argv[1]
    if sys.argv[2] == '1':
        #将fiddler抓包写入LOG_TEST.FIDDLER_BASE_DATA表
        zipdir = sys.argv[3]
        unzipdir = sys.argv[4]
        IBD = IniBaseData(LogTestDBConf, Logger, zipdir, unzipdir)
        IBD.run()
        #将FIDDLER_BASE_DATA表数据写入strategy_edit_fast_regression表
        ATD = analyzeTacticsData(LogTestDBConf, Logger)
        ATD.run()
    elif sys.argv[2] == '2':
        SR = SmokeRunner(dbid, userid, LogTestDBConf, Logger)
        c_idlist = sys.argv[3].decode('gbk').encode('utf-8').split(',')
        SR.run(c_idlist)






