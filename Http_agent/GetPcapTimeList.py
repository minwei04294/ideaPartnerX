#!/usr/bin/env python
# -*- coding: utf-8 -*
# 用于访问MongoDB数据库的公共方法
__author__ = 'wangjun'
#!/usr/bin/env python
#coding=utf-8
#读取pcap文件，解析相应时间戳
import struct,time,traceback
from Common.settings import *
class GetPcapTimeList:
    def __init__(self,filename,logger):
        #日志对象
        self._logger=logger
        #pcap文件名
        self.filename=filename
        #包时间戳集合
        self.packet_data=[]
        #获取时间戳集合
        self.getPcapTimeList()
    def getLocalTime(self,timestamp):
        x = time.gmtime(timestamp)
        return time.strftime('%Y-%m-%d %H:%M:%S',x)
    def getPcapTimeList(self):
        try:
            fpcap = open(self.filename,'rb')
            string_data = fpcap.read()
            #pcap文件的数据包解析
            packet_num = 0
            #数据包头容器
            pcap_packet_header = {}
            #第一个数据包位置
            i =24
            while(i<len(string_data)):

                  #数据包头各个字段
                  pcap_packet_header['GMTtime'] = string_data[i:i+4]
                  pcap_packet_header['len'] = string_data[i+12:i+16]
                  pcap_packet_header['GMTtime'] = self.getLocalTime(struct.unpack('I',pcap_packet_header['GMTtime'])[0])
                  #求出此包的包长len
                  packet_len = struct.unpack('I',pcap_packet_header['len'])[0]
                  #写入此包数据
                  self.packet_data.append({str(packet_num+1):{"GMTtime":pcap_packet_header['GMTtime']}})
                  i = i+ packet_len+16
                  packet_num+=1
        except Exception as e:
            self._logger.Log(u"获取http数据包时间戳集失败：%s" %traceback.format_exc(), InfoLevel.ERROR_Level)

if __name__ == '__main__':
    filename='soursePath/tcpdump.pcap'
    tt=GetPcapTimeList(filename)
    x = tt.packet_data
    for i in x:
        print i