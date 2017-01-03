#!/usr/bin/env python
# -*- coding: utf-8 -*
# 用于访问MongoDB数据库的公共方法
__author__ = 'wangjun'
import re,traceback
from Common.settings import *
from GetPcapTimeList import GetPcapTimeList
try:
    import scapy.all as scapy
except ImportError:
    import scapy,simplejson
try:
    # This import works from the project directory
    import scapy_http.http
except ImportError:
    # If you installed this package via pip, you just need to execute this
    from scapy.layers import http
class getHttpData:
    def __init__(self,filePath,logger):
        #日志对象
        self._logger=logger
        #文件路径
        self.filePath=filePath
        #保存请求集
        self.HttpItems=[]
        #执行数据集获取
        self.getData()
    def getData(self):
        try:
            packets = scapy.rdpcap(self.filePath)
            #获取数据包时间戳集合
            httpTimeList=GetPcapTimeList(self.filePath,self._logger).packet_data
            if not httpTimeList:raise ValueError("获取数据包时间戳集合失败")
            count=0
            for p in packets:
                httpItem={"FileID":None,"HostIP":None,"HttpCode":None,"ReqData":None,"AckData":None,"ReqTime":None,"AckTime":None}
                if 'Raw' in p and p['Raw'] and (re.findall(r'GET .*? HTTP/1.1',p['Raw'].load) or re.findall(r'POST .*? HTTP/1.1',p['Raw'].load)):
                    httpItem["FileID"] = re.findall(r'(?=soursePath/).*?(?=.pcap)',self.filePath)[0].replace("soursePath/","")
                    httpItem["HostIP"] = p['IP'].dst
                    httpItem["HttpCode"] = p['TCP'].ack
                    httpItem["ReqData"] = p['Raw'].load
                    httpItem["AckTime"] = httpTimeList[count][str(count+1)]["GMTtime"]
                    # httpItem["ReqTime"] = p['Raw'].load
                    self.HttpItems.append(httpItem)
                count+=1
        except Exception as e:
            self._logger.Log(u"获取http数据包请求集失败：%s" %traceback.format_exc(), InfoLevel.ERROR_Level)
        try:
            #补登返回集
            count=0
            for HttpItem in self.HttpItems:
                for p in packets:
                    if 'Raw' in p and p['Raw'] and p['Raw'].load and HttpItem["HttpCode"] == p['TCP'].seq:
                        self.HttpItems[count]["AckData"]=p['Raw'].load
                        self.HttpItems[count]["ReqTime"]=httpTimeList[count][str(count+1)]["GMTtime"]
                count+=1
        except Exception as e:
            self._logger.Log(u"补登http数据包返回集失败：%s" %traceback.format_exc(), InfoLevel.ERROR_Level)
if __name__ =="__main__":
    file='soursePath/tcpdump.pcap'
    http=getHttpData(file)
    HttpItems=http.HttpItems
    for http_Item in HttpItems:
        print '=' * 78+'='
        print http_Item["FileID"]
        print '=' * 78+'*'
        print http_Item["HostIP"]
        print '=' * 78+'*'
        print http_Item["HttpCode"]
        print '=' * 78+'*'
        print http_Item["ReqData"]
        print '=' * 78+'*'
        print http_Item["AckData"]
        print '=' * 78+'*'
        print http_Item["ReqTime"]
        print '=' * 78+'*'
        print http_Item["AckTime"]
        print '=' * 78+'='