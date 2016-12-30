#!/usr/bin/env python
# -*- coding: utf-8 -*
# 用于访问MongoDB数据库的公共方法
__author__ = 'wangjun'
#
#
# import pcap, dpkt, dnet
# import sys
#
# class Readpcap():
#     def __init__(self):
#         self.pc = pcap.pcap("aaa.pcap",0,0,False)
#     def printsocket(self):
#         while True:
#             aa = self.pc.next();
#             if(aa == None):
#                 break
#             (ti,pkt ) = aa;
#             ff = dpkt.ethernet.Ethernet(pkt)
#             if(ff.type != 2048):
#                 continue;
#             self.ippkt = ff.data;
#             if self.ippkt.p == 6:
#                 print str(self.ippkt.len)+"\t"+"tcp"
#             elif self.ippkt.p == 17:
#                 print str(self.ippkt.len)+"\t"+"udp"
# def test():
#     mm = Readpcap();
#     mm.printsocket();
# if __name__ == '__main__':
#     test()

#!/usr/bin/env python
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
import re
packets = scapy.rdpcap('soursePath/tcpdump.pcap')
#保存请求集
HttpItems=[]
for p in packets:
    httpItem={"HostIP":None,"HttpCode":None,"ReqData":None,"AckData":None,"ReqTime":None,"AckTime":None}
    if 'Raw' in p and p['Raw'] and (re.findall(r'GET .*? HTTP/1.1',p['Raw'].load) or re.findall(r'POST .*? HTTP/1.1',p['Raw'].load)):
        httpItem["HostIP"] = p['IP'].dst
        httpItem["HttpCode"] = p['TCP'].ack
        httpItem["ReqData"] = p['Raw'].load
        # httpItem["ReqTime"] = p['Raw'].load
        HttpItems.append(httpItem)
#补登返回集
count=0
for HttpItem in HttpItems:
    for p in packets:
        if 'Raw' in p and p['Raw'] and p['Raw'].load and HttpItem["HttpCode"] == p['TCP'].seq:
            HttpItems[count]["AckData"]=p['Raw'].load
    count+=1
for http_Item in HttpItems:
    print '=' * 78+'='
    print http_Item["HostIP"]
    print '=' * 78+'*'
    print http_Item["HttpCode"]
    print '=' * 78+'*'
    print http_Item["ReqData"]
    print '=' * 78+'*'
    print http_Item["AckData"]
    print '=' * 78+'='
for p in packets:
    print '=' * 78
    print p.show()
    # if 'Raw' in  p:
    #     print p.show()
    #     print '*'*78
    #     print p['IP'].src
    #     print p['TCP'].seq
    #     print p['TCP'].ack
    #     print '*'*78
    #     print p['Raw'].load


# #print p.show()
#     for f in p.payload.fields_desc:
#         if f.name == 'src' or f.name == 'dst':
#             ct = scapy.conf.color_theme
#             vcol = ct.field_value
#             fvalue = p.payload.getfieldval(f.name)
#             reprval = f.i2repr(p.payload,fvalue)
#             print "%s : %s" % (f.name, reprval)
#         print f.name
#         #print f.i2repr
#
#     for f in p.payload.payload.fields_desc:
#             if f.name == 'load':
#                 ct = scapy.conf.color_theme
#                 vcol = ct.field_value
#                 fvalue = p.payload.getfieldval(f.name)
#                 reprval = f.i2repr(p.payload,fvalue)
#                 print "%s : %s" % (f.name, reprval)