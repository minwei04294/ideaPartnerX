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
    print u"【指令格式】：大区库dbid;执行人userid;指令类型;参数 ...\n" \
          u"\n" \
          u"【参数说明】\n" \
          u"1、根据fiddler抓包执行数据初始化：\n" \
          u"指令类型: 1\n" \
          u"参数: saz文件所在绝对路径\n" \
          u"【示例】257;3680;1;D:/fiddlerdata\n" \
          u"\n" \
          u"2、根据履历构建的测试数据集id执行测试：\n" \
          u"指令类型: 2\n" \
          u"参数: saz文件名称的列表，英文逗号','分隔\n" \
          u"【示例】257;3680;2;saz_filename1,saz_filename2\n" \
          u"\n" \
          u"【使用说明】\n" \
          u"1、执行时先执行指令类型=1再执行指令类型=2。\n" \
          u"2、执行时，仅需根据需要修改对应的大区库dbid、执行人userID、指令类型、参数即可。\n" \
          u"3、过程中如有路径，请避免路径带空格。"
    print (u"="*60)
    print u"请输入指令："
    cmd = raw_input()
    pars = cmd.split(';')
    dbid = pars[0]
    userid = pars[1]
    cmdtype = pars[2]
    if cmdtype == '1':
        zipdir = pars[3]
        # unzipdir = pars[4]
        unzipdir = os.path.dirname(os.path.realpath(sys.path[0]))+os.sep+'unzipdir'
        if not os.path.exists(unzipdir):
            os.mkdir(unzipdir)
        IBD = IniBaseData(LogTestDBConf, Logger, zipdir, unzipdir)
        IBD.run()
    elif cmdtype == '2':
        SR = SmokeRunner(dbid, userid, LogTestDBConf, Logger)
        c_idlist = pars[3].decode('gbk').encode('utf-8').split(',')
        SR.run(c_idlist)
