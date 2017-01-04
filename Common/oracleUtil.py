#!/usr/bin/env python
# -*- coding: utf-8 -*
# 用于访问Oracle数据库的公共方法
from __builtin__ import isinstance
__author__ = 'wangjun'

import cx_Oracle,traceback
from settings import *
from logger import logger
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

class OracleHelper(object):
    '''用于Oracle数据交互访问'''

    def __init__(self,conn,logger):
        if 'dbname' not in conn:
            sid='orcl'
        else:
            sid=conn['dbname']
        host=conn['host']
        user=conn['user']
        passwd=conn['passwd']
        port=conn['port']
        self._logger = logger
        try:
            self.__dsn=cx_Oracle.makedsn(host,port,sid)
            self.__conn=cx_Oracle.Connection(user=user, password=passwd,dsn=self.__dsn)
            self.__cursor=self.__conn.cursor()
        except Exception as e:
            self._logger.Log('Connect to %s:%s/%s failed: %s' % (host, port, user, e.message), InfoLevel.ERROR_Level)
            exit(0)

    @property
    def conn(self):
        return self.__conn

    @property
    def cursor(self):
        return self.__cursor

    def getColbObject(self):
        return cx_Oracle.CLOB

    def __del__(self):
        try:
            if self.cursor: self.cursor.close()
        except Exception, e:
            self._logger.Log("Close cursor failed: %s" % e, InfoLevel.ERROR_Level)
        try:
            if self.conn: self.conn.close()
        except Exception, e:
            self._logger.Log("Close mysql conn failed: %s" % e, InfoLevel.ERROR_Level)

    def executeSQL(self, sqlcomment):
        '''执行指定sql语句'''
        assert (self.conn)
        assert (self.cursor)
        retResults = []
        retColNames = None
        retRowValues = None
        # 由于插入数据后没有关闭游标，所以会导致插入缓存遗留，这里就是强制缓存无效
        try:
            self._logger.Log(u"Oracle数据库模块执行SQL:{0}".format(sqlcomment))
            self.cursor.execute(sqlcomment)
        except Exception as e:
            self._logger.Log(u"执行语句失败：%s" %traceback.format_exc(), InfoLevel.ERROR_Level)
            return False
        # 若为SELECT语句，则返回查询的结果集
        if sqlcomment.lower().startswith('select'):
            retRowValues = self.cursor.fetchall()
            retColNames = [i[0] for i in self.cursor.description]
            #retResults = self.cursor.fetchmany(numRows=1)
            #转换键值对
            for retRowValue in retRowValues:
                count=0
                rowDict={}
                for retColName in retColNames:
                    if type(retRowValue[count])==str:
                        try :
                            values=retRowValue[count].decode('gbk').encode('utf-8')
                        except :
                            values=retRowValue[count]
                    else:values=retRowValue[count]
                    rowDict.update({retColName:values})
                    count+=1
                retResults.append(rowDict)
        # 否则提交执行
        else:
            self.conn.commit()
            self._logger.Log(u"Oracle数据库模块执行提交成功!!")
        return retResults
    def changeData2WithParam(self,sql,para):
        self._logger.Log(u"Oracle数据库模块执行SQL:%s"%(sql+str(para)))
        self.cursor.prepare(sql)
        self.cursor.execute(None,para)

    def insertData2WithParam(self,sql,para):
        self.cursor.prepare(sql)
        self.cursor.execute(None,para)
    def commitData(self):
        try:
            self.conn.commit()
            self._logger.Log(u"Oracle数据库模块执行提交成功!!")
        except Exception as e:
            self._logger.Log(u"Oracle数据库模块执行提交失败：%s" %traceback.format_exc(), InfoLevel.ERROR_Level)

    def selectData(self,sql):
        try:
            self._logger.Log(u"Oracle数据库模块执行SELECT_SQL:{0}".format(sql))
            self.cursor.execute(sql)
            resultList = []
            retRowValues = self.cursor.fetchall()
            retColNames = [i[0] for i in self.cursor.description]
            for retRowValue in retRowValues:
                count=0
                rowDict={}
                for retColName in retColNames:
                    values = retRowValue[count]
                    rowDict.update({retColName:values})
                    count += 1
                resultList.append(rowDict)
            return resultList
        except Exception:
            self._logger.Log(u"执行select语句失败：%s" %traceback.format_exc(), InfoLevel.ERROR_Level)

    def createDblink(self, dblink_name, destDB_conf):
        conf = destDB_conf
        sql = """
            create database link %s
            connect to %s identified by %s USING
            '(DESCRIPTION = (ADDRESS_LIST = (ADDRESS = (PROTOCOL = TCP)(HOST = %s )(PORT = %s )))(CONNECT_DATA = (SERVICE_NAME = %s )))'
            """ % (dblink_name, conf["user"], conf["passwd"], conf["host"], conf["port"], conf["dbame"])
        try:
            self.cursor.execute(sql)
        except Exception as e:
            self._logger.Log(u"执行语句失败：%s" %e,\
                        InfoLevel.WARNING_Level)
            # raise e

    def dropDblink(self, dblink_name):
        sql = "drop database link %s" % dblink_name
        try:
            self.cursor.execute(sql)
        except Exception as e:
            self._logger.Log(u"执行语句失败：%s" %e,\
                        InfoLevel.WARNING_Level)
            # raise e

if __name__ == '__main__':
    # oracleHelper = OracleHelper('192.168.3.152','GDB250_WJ_TOLLGATE_MK_72','GDB250_WJ_TOLLGATE_MK_72')
    # result = oracleHelper.executeSQL("select LINK_PID,TOLL_INFO from rd_link where link_pid=407162" )
    # print result
    Logger = logger(logfilename)
    oracleobj = OracleHelper(LogTestDBConf, Logger)
    sql = "SELECT DISTINCT L.TYPE, L.LOG_ID FROM strategy_edit_fast_regression l WHERE l.c_id='test-副本'"
    # sql1 = "SELECT COUNT(1) FROM strategy_edit_fast_regression l WHERE l.c_id='test-副本'"
    result = oracleobj.selectData(sql)
    print result
