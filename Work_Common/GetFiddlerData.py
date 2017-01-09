#!/usr/bin/env python
# -*- coding: utf-8 -*

__author__ = 'ZQ'

from Common.settings import *
from Common.logger import *
import os, zipfile, traceback, json, re
import xml.dom.minidom as xdm
from Common.oracleUtil import OracleHelper
from tactics_drivers.EditFastRegressionDriver import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#抓包文件的预处理
class FilesPreprocess():
    def __init__(self, filepath, logger):
        self.filepath = filepath
        self._logger = logger

    #将saz文件后缀改为zip
    def RenameSuffix(self):
        path = self.filepath
        try:
            for filename in os.listdir(path):
                portion = os.path.splitext(filename)
                if portion[1] == '.saz':
                    newname = portion[0] + '.zip'
                    os.rename(os.path.join(path, filename), os.path.join(path, newname))
                elif portion[1] == '.zip':
                    continue
                else:
                    self._logger.Log(u"文件 %s 的后缀不是“.saz”，不执行重命名。" % filename, InfoLevel.INFO_Level)
        except Exception:
            self._logger.Log(u"文件重命名为zip时失败：%s" % traceback.format_exc(), InfoLevel.ERROR_Level)
            raise Exception

    #传入解压后路径，对zip执行解压
    def UnzipFiles(self, zipfilename, unzipdir):
        try:
            fullzipfilename = os.path.abspath(zipfilename)
            fullunzipdir = os.path.abspath(unzipdir)
            self._logger.Log(u"开始压缩 %s 到 %s ..." % (zipfilename.decode('gbk').encode('utf-8'), unzipdir.decode('gbk').encode('utf-8')), InfoLevel.INFO_Level)
            #Check input ...
            if not os.path.exists(fullzipfilename):
                self._logger.Log(u"目录/文件 %s 不存在！" % fullzipfilename.decode('gbk').encode('utf-8'), InfoLevel.INFO_Level)
                raise Exception(u"目录/文件 %s 不存在！")
                # return
            if not os.path.exists(fullunzipdir):
                os.mkdir(fullunzipdir)
            else:
                if os.path.isfile(fullunzipdir):
                    self._logger.Log(u"文件 %s 已存在，执行覆盖！" % fullunzipdir.decode('gbk').encode('utf-8'), InfoLevel.INFO_Level)
                    os.remove(fullunzipdir)
            #Start extract files ...
            srcZip = zipfile.ZipFile(fullzipfilename, "r")
            for eachfile in srcZip.namelist():
                eachfilename = os.path.join(fullunzipdir, eachfile)
                eachdir = os.path.dirname(eachfilename)
                if not os.path.exists(eachdir):
                    os.makedirs(eachdir)
                if not os.path.isdir(eachfilename):
                    fd=open(eachfilename, "wb")
                    fd.write(srcZip.read(eachfile))
                    fd.close()
            srcZip.close()
            self._logger.Log(u"解压 %s 完成！" % zipfilename.decode('gbk').encode('utf-8'), InfoLevel.INFO_Level)
        except Exception:
            self._logger.Log(u"执行解压文件失败：%s" % traceback.format_exc(), InfoLevel.ERROR_Level)
            raise Exception

    #对fiddler文件执行改后缀和解压
    def RunPreprocess(self, unzipdir):
        self.RenameSuffix()
        zipdir = self.filepath
        unzipdir = unzipdir
        for root, dirs, files in os.walk(zipdir):
            for f in files:
                fname = os.path.splitext(f)
                temp_zipdir = zipdir + '\\' + f
                temp_unzipdir = unzipdir + '\\' + fname[0]
                self.UnzipFiles(temp_zipdir, temp_unzipdir)

#解析C/M/S文件得到REQ与ACK
class Analysis():
    def __init__(self, filepath, filename, logger):
        self.filepath = filepath
        self.filename = filename
        self._logger = logger

    #解析C文件得到request
    def AnalysisCfile(self):
        content = {"request": None}
        try:
            with open(os.path.join(self.filepath, self.filename), 'r') as ft:
                lines = ft.readlines()
                for t in lines:
                    # if t.find("GET ") >= 0:
                    #     content["request"] = str(t).replace('GET ', '').replace(' HTTP/1.1', '').replace('\n', '')
                    if t.find("parameter=") >= 0:
                        if t.startswith("GET "):
                            content["request"] = str(t).replace('GET ', '').replace(' HTTP/1.1', '').replace('\n', '')
                        elif t.startswith("parameter="):
                            parm1 = str(t).replace('\n', '')
                            parm2 = ''
                            for p in lines:
                                if p.find("POST ") >= 0:
                                    parm2 = str(p).replace('POST ', '').replace(' HTTP/1.1', '').replace('\n', '')
                            if parm2:
                                content["request"] = parm2 + '&' + parm1
                            else:
                                self._logger.Log(u"未找到POST参数！", InfoLevel.ERROR_Level)
                                raise Exception(u"未找到POST参数！")
        except Exception:
            self._logger.Log(u"解析C文件失败：%s" % traceback.format_exc(), InfoLevel.ERROR_Level)
            raise Exception
        return content

    #解析S文件得到response
    def AnalysisSfile(self):
        response = {"response": None}
        try:
            with open(os.path.join(self.filepath, self.filename), 'r') as ft:
                lines = ft.readlines()
                for t in lines:
                    if re.findall(r"\{\"errmsg+.*",t):
                        response["response"] = json.dumps(re.findall(r"\{\"errmsg+.*",t)[0],sort_keys=True,ensure_ascii=False)
        except Exception:
            self._logger.Log(u"解析S文件失败：%s" % traceback.format_exc(), InfoLevel.ERROR_Level)
            raise Exception
        return response

    #解析M文件得到time
    def AnalysisMfile(self):
        try:
            dom = xdm.parse(os.path.join(self.filepath, self.filename)).documentElement
            message = {"time": None}
            itemlist = dom.getElementsByTagName('SessionTimers')
            item = itemlist[0]
            temp = re.sub(r"\+08:00",'',item.getAttribute("ClientDoneResponse")).replace('T', ' ')
            temp1 = datetime.datetime.strptime(temp[:len(temp)-1],'%Y-%m-%d %H:%M:%S.%f')
            message["time"] = temp1
        except Exception:
            self._logger.Log(u"解析M文件失败：%s" % traceback.format_exc(), InfoLevel.ERROR_Level)
            raise Exception
        return message

#初始化LOG_TEST库中FIDDLER_BASE_DATA表数据
class IniBaseData():
    def __init__(self, conn, logger, zipdir, unzipdir):
        self.oracleObject = OracleHelper(conn, logger)
        self._logger = logger
        self.zipdir = zipdir
        self.unzipdir = unzipdir

    def SplicingAnalysisResult(self):
        inst_col = 'id,REQ,ACK,FILEID,"DATE"'
        sql_insert = "INSERT INTO FIDDLER_BASE_DATA ({0}) values (base_data_id.nextval, :2，:3，:4, :5)".format(inst_col)
        fileidExit_sql = 'SELECT * FROM fiddler_base_data l where l.fileid=\'{0}\''
        try:
            for fileid in os.listdir(self.unzipdir):
                fExit = self.oracleObject.executeSQL(fileidExit_sql.format(fileid).decode('gbk').encode('utf-8'))
                #如果fileid已存在，则不执行insert
                if fExit:
                    self._logger.Log(u"文件 %s 已存在，不执行初始化" % fileid.decode('gbk').encode('utf-8'),InfoLevel.INFO_Level)
                else:
                    #如果fileid不存在，则执行insert
                    filepath = self.unzipdir + '\\' + fileid + '\\raw'
                    #获取路径下文件编号list
                    idlist = []
                    try:
                        for filename in os.listdir(filepath):
                            portion = os.path.splitext(filename)
                            if portion[0][:len(portion[0])-2] not in idlist:
                                idlist.append(portion[0][:len(portion[0])-2])
                    except Exception:
                        self._logger.Log(u"获取路径下文件编号，执行失败: %s" % traceback.format_exc(),InfoLevel.ERROR_Level)
                        raise Exception
                    #按文件编号获取对应的c/m/s
                    try:
                        for i in idlist:
                            fname_c = i + '_c.txt'
                            c = Analysis(filepath, fname_c, self._logger).AnalysisCfile()
                            fname_m = i + '_m.xml'
                            m = Analysis(filepath, fname_m, self._logger).AnalysisMfile()
                            fname_s = i + '_s.txt'
                            s = Analysis(filepath, fname_s, self._logger).AnalysisSfile()
                            self.oracleObject.insertData2WithParam(sql_insert, [c["request"], s["response"], fileid.decode('gbk').encode('utf-8'), m["time"]])
                    except Exception:
                        self._logger.Log(u"按文件编号获取对应的c/m/s，执行失败: %s" % traceback.format_exc(),InfoLevel.ERROR_Level)
                        raise Exception
        except Exception:
            self._logger.Log(u"遍历解析被解压文件异常: %s" % traceback.format_exc(),InfoLevel.ERROR_Level)
            raise Exception
        self.oracleObject.commitData()

    #格式化REQUEST请求数据
    def FormatREQ(self):
        try:
            sql_reqformat = 'UPDATE FIDDLER_BASE_DATA l SET l.REQ=replace(replace(replace(replace(replace(replace(replace(l.REQ,\'%7B\',\'{\'),\'%7D\',\'}\'),\'%22\',\'"\'),\'%5B\',\'[\'),\'%5D\',\']\'),\'%3A\',\':\'),\'%2C\',\',\')'
            self.oracleObject.executeSQL(sql_reqformat)
        except Exception:
            self._logger.Log(u"格式化REQUEST请求数据，执行失败: %s" % traceback.format_exc(),InfoLevel.ERROR_Level)
            raise Exception

    def run(self):
        try:
            self._logger.Log(u"="*60)
            self._logger.Log(u"初始化fiddler数据，执行开始",InfoLevel.INFO_Level)
            self._logger.Log(u"执行解压saz文件",InfoLevel.INFO_Level)
            FilesPreprocess(self.zipdir, self._logger).RunPreprocess(self.unzipdir)
            self._logger.Log(u"执行增量写入FIDDLER_BASE_DATA表",InfoLevel.INFO_Level)
            self.SplicingAnalysisResult()
            self._logger.Log(u"执行格式化REQUEST请求数据",InfoLevel.INFO_Level)
            self.FormatREQ()
            #将FIDDLER_BASE_DATA表数据写入STRATEGY_EDIT_FAST_REGRESSION表
            ATD = analyzeTacticsData(LogTestDBConf, self._logger)
            self._logger.Log(u"执行增量写入STRATEGY_EDIT_FAST_REGRESSION表",InfoLevel.INFO_Level)
            ATD.getTempData()
            self._logger.Log(u"执行中间件扩展字段赋值",InfoLevel.INFO_Level)
            ATD.setTempTypeData()
            self._logger.Log(u"执行中间件编辑类型赋值",InfoLevel.INFO_Level)
            ATD.setTempNewFieldData()
            self._logger.Log(u"执行中间件logid赋值",InfoLevel.INFO_Level)
            ATD.setTempLogidData()
            self._logger.Log(u"初始化fiddler数据，执行结束",InfoLevel.INFO_Level)
            self._logger.Log(u"="*60)
        except Exception:
            self._logger.Log(u"初始化fiddler数据，执行异常: %s" % traceback.format_exc(),InfoLevel.ERROR_Level)

if __name__ == "__main__":
    Logger = logger(logfilename)
    zipdir = 'D:\\fiddler数据'
    unzipdir = 'D:\saz解压'
    FilesPreprocess(zipdir, Logger).RunPreprocess(unzipdir)
    IBD = IniBaseData(LogTestDBConf, Logger, zipdir, unzipdir)
    IBD.SplicingAnalysisResult()