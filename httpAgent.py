#!/usr/bin/env python
# -*- coding: utf-8 -*
__author__ = 'wangjun'

from Common.logger import logger
from Common.settings import *
from Http_agent.CollectHttpData import CollectHttpData
import os,threading,time,ConfigParser
def runCollectHttpData(Logger,DBConnConfig,PcapfilePath,fileCount):
    CollectHttpData(Logger,DBConnConfig,PcapfilePath,fileCount)
def runTcpDump(cmd):
    os.system(cmd)

if __name__ == '__main__':
    #日志对象
    Logger = logger(logfilename)
    cf = ConfigParser.ConfigParser()
    cf.read("conf/httpAgent.ini")
    #pcap文件交互履历
    PcapfilePath=cf.get("config","PcapfilePath")
    if not os.path.exists(PcapfilePath):
         os.mkdir(PcapfilePath)
    #抓包命令
    GetPcapcommand="ping 192.168.4.188 "
    #监控数据库信息:
    DBConnConfig=eval(cf.get("config","DBConnConfig"))
    #批次解析总数
    fileCount=cf.getint("config","fileCount")
    #线程池
    threadpool=[]
    #执行抓包
    #threadpool.append(threading.Thread(target=runTcpDump,args= (GetPcapcommand)))
    #os.system(GetPcapcommand)
    #执行定时解析
    #threadpool.append(threading.Thread(target=runCollectHttpData,args= (Logger,DBConnConfig,PcapfilePath,fileCount)))
    # for td in threadpool:
    #     td.start()

    i=1
    while(i):
        #Logger.Log(u"执行%s"%str(i))
        CollectHttpData(Logger,DBConnConfig,PcapfilePath,fileCount)
        time.sleep(5)
        #i+=1