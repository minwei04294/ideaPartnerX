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

    cmdtype = sys.argv[1]
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