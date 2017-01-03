#!/usr/bin/env python
# -*- coding: utf-8 -*
__author__ = 'wangjun'

from Common.logger import logger
from Common.settings import *
from Http_agent.CollectHttpData import CollectHttpData
import os,threading,time,ConfigParser,time

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
    GetPcapcommand="tcpdump –i {0} -vnn -w  {1} -c 1000"
    #网卡名
    netName=cf.get("config","netName")
    #抓取主机
    Host=cf.get("config","Host")
    #当前时间
    localTime=time.strftime('%Y%m%d')
    #存储文件名
    fileName=(Host.replace(".","_")+'_'+localTime+'_'+netName+"_%sK.pcap")

    filePath=os.path.join(PcapfilePath,fileName)
    #线程池
    i=1
    while(i):
        Logger.Log(u"执行TCPDUMP抓取%s个数据包"%str(i*1000))
        Logger.Log(u"执行命令行:%s"%GetPcapcommand.format(netName,filePath%str(i)))
        runTcpDump(GetPcapcommand.format(netName,filePath%str(i)))
        i+=1
