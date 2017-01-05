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
    #监控主机名
    host=cf.get("config","Host")
    #线程池
    threadpool=[]
    #定期清理历史PCAP文件数量
    rmHisCount=cf.getint("config","rmHisCount")
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
        collect=CollectHttpData(Logger,DBConnConfig,PcapfilePath,fileCount)
        msg=collect.serverMsy(host,IPX_ServerDBConf)
        if msg:
            collect.collect()
            if i==rmHisCount :
                Logger.Log(u"清历史目录(targetPath)!!")
                collect.RemoveTargetPath()
                i=1
        else:
            Logger.Log(u"采集服务端已将我退役,我已无法为您服务!!!")
        time.sleep(5)
        i+=1