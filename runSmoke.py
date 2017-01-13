#!/usr/bin/env python
# -*- coding: utf-8 -*
__author__ = 'ZQ'

from Common.logger import logger
from Common.settings import *
from Work_Common.GetFiddlerData import *
from tactics_drivers.SmokeDriver import *
import sys

if __name__ == '__main__':
    Logger = logger(logfilename)
    print (u"="*60)
    print u"请选择执行内容：\n" \
          u"1、根据fiddler抓包执行数据初始化\n" \
          u"2、根据测试要素执行测试并验证\n"
    print (u"="*60)
    cmdtype = raw_input()
    if cmdtype == '1':
        zipdir = ConfFilename.getElementsByTagName('zipdir')[0].firstChild.data
        unzipdir = os.path.dirname(os.path.realpath(sys.path[0]))+os.sep+'unzipdir'
        if not os.path.exists(unzipdir):
            os.mkdir(unzipdir)
        IniBaseData(LogTestDBConf, Logger, zipdir, unzipdir).run()
    elif cmdtype == '2':
        dbid = ConfFilename.getElementsByTagName('dbid')[0].firstChild.data
        userid = ConfFilename.getElementsByTagName('userid')[0].firstChild.data
        SmokeRunner(dbid, userid, LogTestDBConf, Logger).run()