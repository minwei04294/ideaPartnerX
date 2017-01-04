#!/usr/bin/env python
# -*- coding: utf-8 -*
# 用于访问MongoDB数据库的公共方法
__author__ = 'wangjun'
import os,traceback,shutil,copy,threading
from Common.oracleUtil import OracleHelper
from Common.settings import *
from GetHttpData import getHttpData
class CollectHttpData:
    def __init__(self,logger,conn,filePath,fileCount=10):
        #日志对象
        self._logger=logger
        #数据库连接参数
        self.connConfig=conn
        #连接对象
        self.DBConnect=None
        #Pcap文件读取路径
        self.SoursePath=filePath
        #Pcap文件历史路径
        self.targetPath=filePath.replace("soursePath","targetPath")
        #执行解析文件集:
        self.fileNameList=None
        #一批次解析文件数量
        self.fileCount=fileCount
        #执行
        #self.collect()
    #创建数据库连接
    def connectDB(self):
        self.DBConnect=OracleHelper(self.connConfig,self._logger)
    #提取数据包文件
    def getPcapFile(self):
        #获取解析的Pcap文件列表
        try:
            #获取解析文件名集合
            self.fileNameList=os.listdir(self.SoursePath)
            #排除非pcap文件
            if self.fileNameList:
                fileNames=[]
                for filename in self.fileNameList:
                    if not filename.endswith('.pcap'):continue
                    fileNames.append(filename)
                #文件名排序
                self.fileNameList=copy.deepcopy(fileNames)
                self.fileNameList.sort()
                #数量截取
                self.fileNameList=self.fileNameList[0:self.fileCount]
            #os.path.join(path, newname)
        except Exception:
            self._logger.Log(u"获取文件名集合失败：%s" % traceback.format_exc(), InfoLevel.ERROR_Level)
            raise ValueError("获取文件名集合失败,Pcap文件解析转换过程退出")
    #缓存HTTP数据集
    def getHttpDataList(self,filePath):
        return getHttpData(filePath,self._logger).HttpItems
    #写入数据库
    def setHttpData2DB(self,httpItems):
        insertSql="INSERT INTO HTTP_BASE_DATA(ID,REQ,ACK,FILEID,REQ_DATE,\"DATE\") VALUES(BASE_DATA_ID.NEXTVAL," \
                  "TO_CLOB(:ReqData),TO_CLOB(:AckData),:FileID,TO_DATE(:ReqTime,'yyyy-mm-dd hh24:mi:ss')," \
                  "TO_DATE(:AckTime,'yyyy-mm-dd hh24:mi:ss'))"
        for httpItem in httpItems:
            httpItem.pop("HostIP");httpItem.pop("HttpCode");
            self.DBConnect.changeData2WithParam(insertSql,httpItem)
        self.DBConnect.commitData()
    #执行数据包文件转移
    def PcapFile2BackUp(self,filename):
        filePath=os.path.join(self.SoursePath,filename)
        targetPath=os.path.join(self.targetPath,filename)
        print filePath
        if not os.path.exists(filePath):
            self._logger.Log(u"(soursePath)未找到相应Pcap文件!!")
        else:
            if not os.path.exists(targetPath):
                os.mkdir(targetPath)
            shutil.move(filePath,targetPath)
            self._logger.Log(u"移动Pcap文件到备份路径(targetPath)成功!!")
    #执行解析转换
    def runAnalysis(self,filePath,filename):
        httpItems=self.getHttpDataList(filePath)
        self.setHttpData2DB(httpItems)
        self.PcapFile2BackUp(filename)
    #服务交互
    def serverMsy(self,host,conn):
        try:
            DBconnServer=OracleHelper(conn,self._logger)
            findSql="SELECT STATUS FROM HOST A WHERE A.HOST_NAME='%s'"
            HOST=DBconnServer.executeSQL(findSql%host)
            if not HOST:
                insertSql="INSERT INTO HOST (HOST_ID,HOST_NAME,HOST_TYPE,PARS,CMD,CREATE_TIME,HOST,DB_ID,STATUS)" \
                          "VALUES (HOSTID.NEXTVAL,'%s','HttpAgent',NULL,NULL,SYSDATE,'%s',0,0)"
                DBconnServer.executeSQL(insertSql%(host,host))
                return True
            elif HOST[0]['STATUS']=='0':
                return True
            elif HOST[0]['STATUS']=='1':
                return False
        except Exception as e:
            self._logger.Log(u"代理与服务交互失败,失败原因:%s"%traceback.format_exc(1),InfoLevel.ERROR_Level)
            return False
    #继承执行
    def collect(self):
        #10个文件为一批解析
        try:
            self.connectDB()
            self.getPcapFile()
            if self.fileNameList:
                #执行解析
                threadpool=[]
                for filename in self.fileNameList:
                    filePath=os.path.join(self.SoursePath,filename)
                    self.runAnalysis(filePath,filename)
                #多线程
                #     th = threading.Thread(target= self.runAnalysis,args= (filePath,filename))
                #     threadpool.append(th)
                # for th in threadpool:
                #     th.start()
            else:
                self._logger.Log(u"未获取到有效文件名集合,Pcap文件解析转换过程退出")
        except Exception:
            self._logger.Log(u"Pcap文件解析转换过程失败：%s" % traceback.format_exc(), InfoLevel.ERROR_Level)
        #开启多线程解析


from Common.logger import logger
from Common.settings import *

if __name__ == '__main__':
    #日志对象
    Logger = logger(logfilename)
    #pcap文件交互履历
    PcapfilePath="/Users/wangjun/Workspace/GitHub/ideaPartnerX-master/Http_agent/soursePath"

    #抓包命令
    GetPcapcommand=""
    #监控数据库信息:
    DBConnConfig={
        "dbname":"orcl",
        "host":"192.168.4.131",
        "user":"LOG_TEST",
        "passwd":"LOG_TEST",
        "port":"1521"
    }
    #批次解析总数
    fileCount=10
    #执行抓包
    #os.system(GetPcapcommand)
    #执行定时解析
    CollectHttpData(Logger,DBConnConfig,PcapfilePath,fileCount)