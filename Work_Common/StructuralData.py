#!/usr/bin/env python
# -*- coding: utf-8 -*
# 用于访问MongoDB数据库的公共方法
__author__ = 'wangjun'
import json,cx_Oracle,struct,json,copy,traceback,os
from STAF_Common.settings import InfoLevel
#from oracleUtil import OracleHelper
#from mongoUtil import MongodbHelper
class CreateGeoData:
    def __init__(self,DrawListString):
        self.GeoIntermediateData=self.CommandDrawGraph(DrawListString)
    def CommandDrawGraph(self,DrawListString):
        DrawList=[]
        GeoIntermediateData=[]
        DatumPointX=0;DatumPointY=0
        DrawStringList=DrawListString.split(",")
        for draw in DrawStringList:
            point=draw.split("#")
            if point[0]!='P':
                point[1]=int(point[1])
                DrawList.append({point[0]:point[1]})
            else:
                DrawList.append({point[0]:point[1]})
        for DrawPoint in DrawList:
            if 'XY' in DrawPoint:
                DatumPointX+=DrawPoint['XY']
                DatumPointY+=DrawPoint['XY']
            elif 'X' in DrawPoint:
                DatumPointX+=DrawPoint['X']
            elif 'Y' in DrawPoint:
                DatumPointY+=DrawPoint['Y']
            elif 'P' in DrawPoint:
                DatumPointX+=int(DrawPoint['P'].split('.')[0])
                DatumPointY+=int(DrawPoint['P'].split('.')[1])
            GeoIntermediateData.append([DatumPointX,DatumPointY])
        return GeoIntermediateData
class GeoTemp2Geometry:
    #GRID分份 X800  Y534
    def __init__(self,PointList,DatumPoint):
        self.PointList=PointList
        self.GeoData=[]
        self.stepLenght=0.000039
        self.ToGeometry(DatumPoint)
    def ToGeometry(self,DatumPoint):
        for Point in self.PointList:
            XY=0
            for Geo in Point:
                if not XY:
                    self.GeoData.append(Geo*self.stepLenght+DatumPoint[0])
                else:
                    self.GeoData.append(Geo*self.stepLenght+DatumPoint[1])
                XY+=1
        return self.GeoData
class StructuralOraDataForGDB:
    def __init__(self,OracleObject,Model,grid,Mongo):
        self.grid=grid
        self.attributeData=copy.deepcopy(Model)
        self.differenceData=copy.deepcopy(Model['DIFFERENCE_DATA'])
        self.globalData=Model['GLOBAL_DATA']
        self.RelationData=copy.deepcopy(Model['RELATION'])
        self.OracleObject=OracleObject
        self.MongoObject=Mongo
        self.RowID=0
    #--读取数据
    def readOracleData(self,sql):
        Rows=self.OracleObject.executeSQL(sql)
        return Rows[0]
    #--处理数据库关键字
    def changeKeyWordForOracle(self,Row):
        keyNames=['LEVEL']
        for keyName in keyNames:
            if keyName in Row:
                Row['\"'+keyName+'\"']=Row[keyName]
                Row.pop(keyName)
    #--差异值替换
    def replaceKeyValues(self,Row,defineData):
        if 'ROW_ID' in Row:
            #Row['ROW_ID']=hex(201408181930)
            Row.pop('ROW_ID')
        if 'GEO_TEMP' in defineData:
            defineData.pop('GEO_TEMP')
        for keyName in defineData:
            if keyName in Row:
                Row[keyName]=defineData[keyName]
            else:
                print '%s属性字段不存在，请确认字段正确性'%(keyName)
    def geometry2String(self,GEOMETRY):
        SDO_GTYPE=str(GEOMETRY.SDO_GTYPE)
        SDO_SRID=str(GEOMETRY.SDO_SRID)
        #node
        if GEOMETRY.SDO_GTYPE==2001:
            SDO_POINT_TYPE='MDSYS.SDO_POINT_TYPE(%s,%s,NULL)'%(str(GEOMETRY.SDO_POINT.X),str(GEOMETRY.SDO_POINT.Y))
            SDO_ELEM_INFO_ARRAY='NULL'
            SDO_ORDINATE_ARRAY='NULL'
        else:
            SDO_POINT_TYPE='NULL'
            SDO_ELEM_INFO_ARRAY='MDSYS.SDO_ELEM_INFO_ARRAY(%s)'%(','.join([str(Point) for Point in GEOMETRY.SDO_ELEM_INFO]))
            SDO_ORDINATE_ARRAY='MDSYS.SDO_ORDINATE_ARRAY(%s)'%(','.join([str(Point) for Point in GEOMETRY.SDO_ORDINATES]))
        GeoStringValue='MDSYS.SDO_GEOMETRY(%s,%s,%s,%s,%s)' %(SDO_GTYPE,SDO_SRID,SDO_POINT_TYPE,SDO_ELEM_INFO_ARRAY,SDO_ORDINATE_ARRAY)
        return GeoStringValue
    #写人数据
    def writeOracleData(self,Row,gemometry,tableName):
        colList0=str(Row.keys()).replace('[',':').replace(']','').replace(',',',:').replace("'","")
        colList1=str(Row.keys()).replace('[','').replace(']','').replace("'","")
        if self.RowID<10:
            count='00'+str(self.RowID)
        if self.RowID<100 and self.RowID>9:
            count='0'+str(self.RowID)
        rowCode=str(self.grid)+count
        if gemometry:
            SqL=u'insert into %s (ROW_ID,GEOMETRY,%s) values(HEXTORAW(%s),%s,%s)' %(tableName,colList1,rowCode,gemometry,colList0)
        else:
            SqL=u'insert into %s (ROW_ID,%s) values(HEXTORAW(%s),%s)' %(tableName,colList1,rowCode,colList0)
        print SqL
        self.RowID+=1
        return SqL
    #替换坐标
    def replaceGeometry(self,Geometry,SDO_ORDINATES):
        GEOMETRY=struct
        GEOMETRY.SDO_GTYPE=Geometry.SDO_GTYPE
        GEOMETRY.SDO_SRID=Geometry.SDO_SRID
        GEOMETRY.SDO_POINT=struct
        GEOMETRY.SDO_ELEM_INFO=Geometry.SDO_ELEM_INFO
        GEOMETRY.SDO_ORDINATES=Geometry.SDO_ORDINATES
        if len(SDO_ORDINATES)==2:
            GEOMETRY.SDO_POINT.X=SDO_ORDINATES[0]
            GEOMETRY.SDO_POINT.Y=SDO_ORDINATES[1]
            GEOMETRY.SDO_ORDINATES='NULL'
        else:
            GEOMETRY.SDO_ORDINATES=SDO_ORDINATES
        return GEOMETRY
    #获取基准坐标
    def getPoint(self):
        PointList=grid2geo(self.grid)
        return [PointList[0],PointList[1]]
    #转换记忆数据
    def getMemoryData(self,desc):
        self.attributeData['KEY_NAME_DESC']=desc
        self.attributeData['DATA_TYPE']='CREATE_DATA'
    #记忆数据
    def MemoryDataForMongo(self):
        self.MongoObject.MemoryGDB(self.attributeData)
    #执行构建
    def CreateData(self):
        #解析Model
        #重构几何
        for ModelRow in self.differenceData:
            tableCount=0
            for DataRow in self.differenceData[ModelRow]:
                if 'GEO_TEMP' in DataRow:
                    geoTemp2=CreateGeoData(DataRow['GEO_TEMP'])
                    Geo=GeoTemp2Geometry(geoTemp2.GeoIntermediateData,self.getPoint())
                    self.differenceData[ModelRow][tableCount]['GEO_TEMP']=Geo.GeoData
                tableCount+=1
            #合并属性
            tableGlobalCount=0
            for ModelGlobalRow in self.globalData:
                if ModelRow in ModelGlobalRow:
                    tableCount1=0
                    for data in self.differenceData[ModelRow]:
                        GlobalRow=self.globalData[tableGlobalCount][ModelRow]
                        for key in data:
                            if key in GlobalRow:
                                GlobalRow.pop(key)
                        self.differenceData[ModelRow][tableCount1].update(GlobalRow)
                        print data
                tableGlobalCount+=1
        #循环执行构建
        for Command in self.differenceData:
            Sql=u'SELECT * FROM %s WHERE ROWNUM=1'%(Command)

            for ModelDataRow in self.differenceData[Command] :
                Row=self.readOracleData(Sql)
                self.changeKeyWordForOracle(Row)
                if 'ROW_ID' in Row:Row.pop('ROW_ID')
                if 'GEO_TEMP' in ModelDataRow and 'GEOMETRY' in Row:
                    GEOMETRY=self.replaceGeometry(Row['GEOMETRY'],ModelDataRow['GEO_TEMP'])
                    gemometry=self.geometry2String(GEOMETRY)
                    Row.pop('GEOMETRY')
                    SQL=self.writeOracleData(Row,gemometry,Command)
                else:
                    SQL=self.writeOracleData(Row,None,Command)
                self.replaceKeyValues(Row,ModelDataRow)
                for key in Row:
                    if type(Row[key])==long:
                        print "存在长整型数据，可能导致数据错误"
                self.OracleObject.insertData2WithParam(SQL,Row)
        self.OracleObject.conn.commit()
class RemoveData:
    def __init__(self,OracleObject,grid,tableList):
        self.OracleObject=OracleObject
        self.grid=grid
        self.tableList=tableList
        self.run()
    def run(self):
        for tableName in self.tableList:
            Sql=u"DELETE FROM %s WHERE ROW_ID LIKE \'%s%%\'"%(tableName,'0'+str(self.grid))
            print Sql
            self.OracleObject.executeSQL(Sql)
class AutoCreateModel:
    def __int__(self,PID,ModelTemp):
        self.Relation=None
        self.GlobalData=None
        self.DifferenceData=None
        self.Model={}
        self.ModelTemp=ModelTemp
        self.PointList=['RD_NODE','RW_NODE']
        self.LinkList=['RD_LINK']
        self.PolgonList=[]
    # def ComputingEndPoint(self,string):
    #     endPoint=None;DatumPointX=0;DatumPointY=0
    #     PointTempList=string.split(",")
    #     startPoint=PointTempList[0]
    #     for Point in PointTempList:
    #         PointXY=Point.split("#")
    #         if 'XY' in PointXY[0]:
    #             DatumPointX+=PointXY[0]['XY']
    #             DatumPointY+=PointXY[0]['XY']
    #         elif 'X' in PointXY[0]:
    #             DatumPointX+=PointXY[0]['X']
    #         elif 'Y' in PointXY[0]:
    #             DatumPointY+=PointXY[0]['Y']
    #     if DatumPointX==DatumPointY:
    #         endPoint="XY#"+str(DatumPointY)
    #     else:
    #         endPoint="P#"+str(DatumPointX)+"."+str(DatumPointY)
    #     return startPoint,endPoint
    # def CreateDifferenceData(self):
    #     self.Relation=copy.deepcopy(self.ModelTemp['RELATION'])
    #     self.DifferenceData=copy.deepcopy(self.ModelTemp['DIFFERENCE_DATA'])
    #     for TableName in self.DifferenceData:
    #         if TableName in self.LinkList:
    #             for row in self.DifferenceData[TableName]:
    #                 if 'GEO_TEMP' in row:
    #
    #
    #
    # c={"RELATION":{"RD_NODE":{"NODE_PID":0,"CHILD_TABLE":{"RD_LINK":{"LINK_PID":0,"S_NODE_PID":1,"E_NODE_PID":1}}}},
    # "GLOBAL_DATA":[{"RD_NODE":{"KIND":1,"ADAS_FLAG":0}},{"RD_LINK":{"KIND":7,"DIRECT":2,"MESH_ID":'605605'}}],
    # "DIFFERENCE_DATA":{"RD_NODE":[{"GEO_TEMP":None},{"GEO_TEM P":None}],
    #                     "RD_LINK":[{"LINK_PID":22920006,"GEO_TEMP":"XY#25,Y#25"}]}}
class Build:
    def __init__(self,Data,Ora,Mon):
        RemoveData(Ora,Data['GRID'],Data['DATA']["DIFFERENCE_DATA"].keys())
        RemoveDataWithLog(Data['GRID'],Data['USER_ID'],Ora)
        run=StructuralOraDataForGDB(Ora,Data['DATA'],Data['GRID'],Mon)
        run.CreateData()
        run.getMemoryData(Data['KEY_DESC'])
        run.MemoryDataForMongo()
class RemoveDataWithLog:
    def __init__(self,grid,userid,oracleOject,case_id="caseid111"):
        self.grid=grid
        self.userid=userid
        self.oracleOject=oracleOject
        self.caseid=case_id
        self.run()
    def backupLogTable(self):
        #备份表存在么？清除库中数据
        CharLength='00000000000000000000000000000000000000000000000000'
        FindBackTableSql="SELECT T.TABLE_NAME FROM USER_TABLES T WHERE T.TABLE_NAME IN ('LOG_OPERATION_DT_BAK','LOG_DETAIL_DT_BAK','LOG_DETAIL_GRID_DT_BAK')"
        BackLogOperationSql="CREATE TABLE LOG_OPERATION_DT_BAK AS SELECT A.*,'%s'AS CASEID FROM LOG_OPERATION A WHERE ROWNUM=0"%(CharLength)
        BackLogDeiailSql="CREATE TABLE LOG_DETAIL_DT_BAK AS SELECT * FROM LOG_DETAIL WHERE ROWNUM=0"
        BackLogDeiailGridSql="CREATE TABLE LOG_DETAIL_GRID_DT_BAK AS SELECT * FROM LOG_DETAIL_GRID WHERE ROWNUM=0"
        BackSqlList={"LOG_OPERATION_DT_BAK":BackLogOperationSql,"LOG_DETAIL_DT_BAK":BackLogDeiailSql,"LOG_DETAIL_GRID_DT_BAK":BackLogDeiailGridSql}
        BackUpTabNameList=self.oracleOject.executeSQL(FindBackTableSql)
        if BackUpTabNameList:
            for BackUpTabName in BackUpTabNameList:
                if BackUpTabName['TABLE_NAME'] in BackSqlList:
                    BackSqlList.pop(BackUpTabName['TABLE_NAME'])
        if len(BackSqlList)!=0:
            for BackTabName in BackSqlList:
                self.oracleOject.executeSQL(BackSqlList[BackTabName])
    def removeDataByGrid(self):
        #提出表和row_id
        deleteConditionSql="SELECT D.TB_NM,RAWTOHEX(D.TB_ROW_ID) FROM LOG_DETAIL D " \
                           "WHERE D.OP_ID IN" \
                           "(SELECT C.OP_ID FROM LOG_OPERATION C" \
                           " WHERE C.OP_ID IN (SELECT B.OP_ID " \
                           "FROM LOG_DETAIL B WHERE B.ROW_ID IN " \
                           "(SELECT A.LOG_ROW_ID FROM LOG_DETAIL_GRID A WHERE A.GRID_ID = %s)) AND C.US_ID='%s') AND D.OP_TP=1"%(str(self.grid),str(self.userid))
        deleteConditionList=self.oracleOject.executeSQL(deleteConditionSql)
        if len(deleteConditionList)!=0:
            for Condition in deleteConditionList:
                deleteSql="DELETE  FROM %s WHERE ROW_ID='%s'"%(Condition['TB_NM'],Condition['RAWTOHEX(D.TB_ROW_ID)'])
                print deleteSql
                self.oracleOject.executeSQL(deleteSql)
    def backUpData(self):
        #提取LOG后清除
        OperationSql="FROM LOG_OPERATION C WHERE C.OP_ID IN (SELECT B.OP_ID  FROM LOG_DETAIL B  WHERE B.ROW_ID IN (SELECT A.LOG_ROW_ID   FROM LOG_DETAIL_GRID A WHERE A.GRID_ID = %s)) AND C.US_ID='%s'"%(str(self.grid),str(self.userid))
        backUpOperationSql="INSERT INTO LOG_OPERATION_DT_BAK SELECT C.*,'%s' AS CASEID %s"%(self.caseid,OperationSql)
        deleteOperationSql="DELETE %s"%(OperationSql)
        backUpDetailSql="INSERT INTO LOG_DETAIL_DT_BAK SELECT B.* FROM LOG_DETAIL B WHERE B.OP_ID IN (SELECT C.OP_ID FROM LOG_OPERATION_DT_BAK  C)"
        deleteDetailSql="DELETE FROM LOG_DETAIL B WHERE B.OP_ID IN (SELECT C.OP_ID FROM LOG_OPERATION_DT_BAK  C)"
        backUpDetailGridSql="INSERT INTO LOG_DETAIL_GRID_DT_BAK SELECT * FROM LOG_DETAIL_GRID B WHERE B.LOG_ROW_ID IN (SELECT C.ROW_ID FROM LOG_DETAIL_DT_BAK C)"
        deleteDetailGridSql="DELETE FROM LOG_DETAIL_GRID B WHERE B.LOG_ROW_ID IN (SELECT C.ROW_ID FROM LOG_DETAIL_DT_BAK C)"
        backlist=[backUpOperationSql,backUpDetailSql,backUpDetailGridSql]
        deletelist=[deleteDetailGridSql,deleteDetailSql,deleteOperationSql]
        for back in backlist:
            print back
            self.oracleOject.executeSQL(back)
        for delete in deletelist:
            print delete
            self.oracleOject.executeSQL(delete)
    def run(self):
        self.backupLogTable()
        self.removeDataByGrid()
        self.backUpData()
#履历数据管理
class logDataManage:
    def __init__(self,oracleObjectSyslog,oracleObjectRegion,Conn,grid,user_id,data_set_id,logger):
        self.oracleObjectSyslog=oracleObjectSyslog
        self.oracleObjectRegion=oracleObjectRegion
        self.Conn=Conn
        self.grid=grid
        self.user_id=user_id
        self.data_set_id=data_set_id
        self._logger=logger
    #继承履历
    def inheritLog(self):
        logExtract(self.Conn,self.oracleObjectRegion,self.oracleObjectSyslog,self.grid,self.user_id,self.data_set_id,'backLog',self._logger)
    #清除履历
    def cleanLog(self):
        logExtract(self.Conn,self.oracleObjectRegion,self.oracleObjectSyslog,self.grid,self.user_id,self.data_set_id,'cleanSource',self._logger)
    #构建数据
    def structuralData(self):
        RowIds=logExtract(self.Conn,self.oracleObjectRegion,self.oracleObjectSyslog,self.grid,self.user_id,self.data_set_id,'getRowIds',self._logger)
        logAnalyze(RowIds.rowIds,self.oracleObjectSyslog,self.oracleObjectRegion,0,self._logger)

    #回滚构建数据
    def rollbackData(self):
        RowIds=logExtract(self.Conn,self.oracleObjectRegion,self.oracleObjectSyslog,self.grid,self.user_id,self.data_set_id,'getRowIds',self._logger)
        logAnalyze(RowIds.rowIds,self.oracleObjectSyslog,self.oracleObjectRegion,1,self._logger)
    #回滚大区数据
    def rollbackRegionData(self):
        RowIds=logExtract(self.Conn,self.oracleObjectRegion,self.oracleObjectSyslog,self.grid,self.user_id,self.data_set_id,'getRegionRowIds',self._logger)
        logAnalyze(RowIds.rowIds,self.oracleObjectRegion,self.oracleObjectRegion,1,self._logger)
#履历获取
class logExtract:
    def __init__(self,Conn,oracleObjectOne,oracleObjectTwo,grid,user_id,data_set_id,extractType,logger):
        self.extractType=extractType
        self.oracleObjectOneConn=Conn
        self.oracleObjectOne=oracleObjectOne
        self.oracleObjectTwo=oracleObjectTwo
        self.DBLinkName=None
        self.grid=grid
        self.user_id=user_id
        self.date_time=None
        self.data_set_id=data_set_id
        self.rowIds=[]
        self._logger=logger
        self.run()

    #来源库创建DBlink
    def createDBLink(self):
        FindDBlinkSql="SELECT * FROM ALL_DB_LINKS WHERE DB_LINK IN ('%s')"
        #DropDBlinkSql="DROP DATABASE LINK %s"
        CreateDBLinkSql="CREATE DATABASE LINK %s CONNECT TO %s IDENTIFIED BY %s USING '(DESCRIPTION = (ADDRESS_LIST = (ADDRESS = (PROTOCOL = TCP)(HOST = %s )(PORT = %s )))(CONNECT_DATA = (SERVICE_NAME = %s )))'"
        existFlag=self.oracleObjectTwo.executeSQL(FindDBlinkSql%self.oracleObjectOneConn['user'].upper())
        if not existFlag:
            self.oracleObjectTwo.executeSQL(CreateDBLinkSql%(self.oracleObjectOneConn['user'].upper(),
                                                             self.oracleObjectOneConn['user'],
                                                             self.oracleObjectOneConn['passwd'],
                                                             self.oracleObjectOneConn['host'],
                                                             str(self.oracleObjectOneConn['port']),
                                                             self.oracleObjectOneConn['dbname']
            ))
        self.DBLinkName=self.oracleObjectOneConn['user'].upper()
    #根据grid、userid取履历
    def getRowIdsWithGridAndUserId(self):
        try:
            #,TO_NUMBER(TO_CHAR(SYSDATE, 'YYYYMMDDHH24MI'))+TO_NUMBER(RANK () OVER (ORDER BY ROWNUM))  AS SEQ
            #OperationSql="FROM LOG_OPERATION@DB_LINK C WHERE C.OP_ID IN (SELECT B.OP_ID  FROM LOG_DETAIL@DB_LINK B  WHERE B.ROW_ID IN (SELECT A.LOG_ROW_ID   FROM LOG_DETAIL_GRID@DB_LINK A WHERE A.GRID_TYPE=1 AND A.GRID_ID = %s)) AND C.US_ID='%s'"%(str(self.grid),str(self.user_id))
            OperationSql="FROM LOG_ACTION@DB_LINK A,LOG_OPERATION@DB_LINK B,LOG_DETAIL@DB_LINK C,LOG_DETAIL_GRID@DB_LINK D " \
                         "WHERE A.ACT_ID = B.ACT_ID AND B.OP_ID = C.OP_ID AND C.ROW_ID = D.LOG_ROW_ID AND A.US_ID = %s AND D.GRID_ID = %s " \
                         "AND B.OP_ID NOT IN ( SELECT E.OP_ID FROM LOG_OPERATION E WHERE  E.DATA_SET_ID='%s')"%(str(self.user_id),str(self.grid),self.data_set_id)
            backUpActionSql="INSERT INTO LOG_ACTION SELECT T.*,'%s' AS DATA_SET_ID,SYSDATE AS INIT_DATE FROM  LOG_ACTION@DB_LINK T WHERE T.ACT_ID IN (SELECT A.ACT_ID %s)"%(self.data_set_id,OperationSql)
            backUpOperationSql="INSERT INTO LOG_OPERATION SELECT  T.*,'%s' AS DATA_SET_ID FROM  LOG_OPERATION@DB_LINK T WHERE T.OP_ID IN (SELECT B.OP_ID %s)"%(self.data_set_id,OperationSql)
            backUpDetailSql="INSERT INTO LOG_DETAIL SELECT  T.*,'%s' AS DATA_SET_ID  FROM  LOG_DETAIL@DB_LINK T WHERE T.OP_ID IN (SELECT B.OP_ID %s)"%(self.data_set_id,OperationSql)
            backUpDetailGridSql="INSERT INTO LOG_DETAIL_GRID SELECT  T.*,'%s' AS DATA_SET_ID  FROM  LOG_DETAIL_GRID@DB_LINK T WHERE T.LOG_ROW_ID IN (SELECT C.ROW_ID %s )"%(self.data_set_id,OperationSql)
            backlist=[backUpDetailGridSql,backUpDetailSql,backUpActionSql,backUpOperationSql]
            for backSql in backlist:
                backSql=backSql.replace('DB_LINK',self.DBLinkName)
                print backSql
                self.oracleObjectTwo.cursor.execute(backSql)
            #提交事务
            self.oracleObjectTwo.conn.commit()
        except Exception as e:
            self._logger.Log(u'执行履历数据提取失败，原因是：%s'%(traceback.format_exc(1)),InfoLevel.ERROR_Level)
            print '执行履历数据提取失败，原因是：%s'%(traceback.format_exc(1))
            self.oracleObjectTwo.conn.rollback()
    #提取系统detailid
    def getLogDetailId(self):
        DetailRowids=[]
        #logSql="SELECT RAWTOHEX(A.ROW_ID) FROM LOG_DETAIL A WHERE A.DATA_SET_ID='%s'"
        #logSql="SELECT RAWTOHEX(A.ROW_ID) FROM LOG_DETAIL_BAK A WHERE A.DATA_SET_ID='%s' ORDER BY SEQ"
        logSql="SELECT RAWTOHEX(A.ROW_ID) FROM LOG_DETAIL A ,LOG_OPERATION B WHERE A.OP_ID=B.OP_ID AND A.DATA_SET_ID='%s' AND B.DATA_SET_ID=A.DATA_SET_ID ORDER BY B.OP_DT,B.OP_SEQ ASC"
        LogDetailRowids=self.oracleObjectTwo.executeSQL(logSql%self.data_set_id)
        if len(LogDetailRowids)==0:
            self._logger.Log(u'履历库中未找到相关履历,查找语句:%s'%(logSql%self.data_set_id),InfoLevel.ERROR_Level)
        for Rowid in LogDetailRowids:
            DetailRowids.append(Rowid['RAWTOHEX(A.ROW_ID)'])
        self.rowIds=DetailRowids
    #提取大区库
    def getRegionLogDetailId(self):
        DetailRowids=[]
        BaseSql="FROM LOG_ACTION A,LOG_OPERATION B,LOG_DETAIL C,LOG_DETAIL_GRID D1 WHERE A.ACT_ID = B.ACT_ID AND B.OP_ID = C.OP_ID AND C.ROW_ID = D1.LOG_ROW_ID AND A.US_ID = %s AND D1.GRID_ID = %s"%(str(self.user_id),str(self.grid))
        logSql="SELECT RAWTOHEX(D.ROW_ID) FROM LOG_DETAIL D WHERE D.OP_ID IN (SELECT B.OP_ID %s)"%BaseSql
        LogDetailRowids=self.oracleObjectOne.executeSQL(logSql)
        if len(LogDetailRowids)==0:
            self._logger.Log(u'大区库中grid=%s未找到相关履历,查找语句:%s'%(str(self.grid),logSql),InfoLevel.INFO_Level)
        for Rowid in LogDetailRowids:
            DetailRowids.append(Rowid['RAWTOHEX(D.ROW_ID)'])
        self.rowIds=DetailRowids
    #清除grid、userid履历
    def cleanSourceLog(self):
        try:
            #OperationSql="DELETE FROM LOG_DETAIL WHERE EXISTS(SELECT 1 FROM LOG_DETAIL T,LOG_OPERATION A,LOG_DETAIL_GRID B WHERE T.OP_ID=A.OP_ID AND T.ROW_ID = B.LOG_ROW_ID AND A.US_ID='%s' AND B.GRID_ID=%s );char(10) DELETE FROM LOG_OPERATION A WHERE A.OP_ID NOT IN (SELECT B.OP_ID FROM LOG_DETAIL B);char(10) DELETE FROM LOG_DETAIL_GRID A WHERE A.LOG_ROW_ID NOT IN (SELECT B.ROW_ID FROM LOG_DETAIL B);"%(str(self.user_id),str(self.grid))
            BaseSql="FROM LOG_OPERATION B,LOG_DETAIL C,LOG_DETAIL_GRID D WHERE A.ACT_ID = B.ACT_ID AND B.OP_ID = C.OP_ID AND C.ROW_ID = D.LOG_ROW_ID AND A.US_ID = %s AND D.GRID_ID = %s"%(str(self.user_id),str(self.grid))
            deleteActonSql="DELETE FROM  LOG_ACTION A WHERE EXISTS(SELECT 1 %s)"%BaseSql
            deleteOperationSql="DELETE FROM  LOG_OPERATION T WHERE T.ACT_ID NOT IN (SELECT A.ACT_ID FROM LOG_ACTION A)"
            deleteDetailSql="DELETE FROM  LOG_DETAIL T WHERE T.OP_ID NOT IN (SELECT A.OP_ID FROM LOG_OPERATION A)"
            deleteDetailGridSql="DELETE FROM  LOG_DETAIL_GRID T WHERE T.LOG_ROW_ID NOT IN (SELECT A.ROW_ID FROM  LOG_DETAIL A)"
            deletelist=[deleteActonSql,deleteOperationSql,deleteDetailSql,deleteDetailGridSql]
            backTabName=['LOG_ACTION','LOG_OPERATION','LOG_DETAIL','LOG_DETAIL_GRID']
            dropTab='DROP TABLE {0}_BAK';createBakTab='CREATE TABLE {0}_BAK AS SELECT * FROM {1}'
            for tableName in backTabName:
                try:
                    self.oracleObjectOne.cursor.execute(dropTab.format(tableName))
                except Exception as e:
                    self._logger.Log(u"清楚备份表失败,原因:%s"%e)
                self.oracleObjectOne.cursor.execute(createBakTab.format(tableName,tableName))
            for delete in deletelist:
                print delete
                self.oracleObjectOne.cursor.execute(delete)
            #self.oracleObjectOne.cursor.execute(OperationSql)
            #提交事务
            self.oracleObjectOne.conn.commit()
        except Exception as e:
            self._logger.Log(u'执行履历按grid+userid数据清除失败，原因是：%s'%(traceback.format_exc(1)),InfoLevel.ERROR_Level)
            print u'执行履历按grid+userid数据清除失败，原因是：%s'%(traceback.format_exc(1))
            self.oracleObjectOne.conn.rollback()
            exit(1)
    #履历处理
    def run(self):
        if self.extractType=='backLog':
            self.createDBLink()
            self.getRowIdsWithGridAndUserId()
        elif self.extractType=='cleanSource':
            self.cleanSourceLog()
        elif self.extractType=='getRowIds':
            self.getLogDetailId()
        elif self.extractType=='getRegionRowIds':
            self.getRegionLogDetailId()
    #根据grid、userid、date_time提取履历

#履历解析
class logAnalyze:
    def __init__(self,rowidList,oracleObject,oracleObjectTwo,Type,logger):
        #analyzeType值域:回滚：1；构建：0；默认；0
        self.analyzeType=Type
        self.rowidList=rowidList
        self.oracleObject=oracleObject
        self.oracleObjectTwo=oracleObjectTwo
        self.oracleSqlList=[]
        self._logger=logger
        self.getLogData()
    #获取履历实体
    def getLogData(self):
        DetailSql="SELECT TB_NM,TO_CHAR(OLD),TO_CHAR(NEW),RAWTOHEX(TB_ROW_ID),OP_TP,FD_LST,OB_PID FROM LOG_DETAIL T WHERE RAWTOHEX(ROW_ID)='%s'"
        self._logger.Log(u'开始解析履历数据生成语句')
        for rowid in  self.rowidList:
            print DetailSql%rowid
            SqlResult=self.oracleObject.executeSQL(DetailSql%rowid)
            Sql,Param=self.spliceSql(SqlResult[0])
            self.oracleSqlList.append([Sql,Param])
        oracleSqlList=copy.deepcopy(self.oracleSqlList)
        #构建
        if not self.analyzeType:
            self._logger.Log(u'开始构建数据.........')
            oraDataHand(self.oracleObjectTwo,oracleSqlList,self._logger)
            self._logger.Log(u'构建数据成功.........')
        #回滚
        else:
            self._logger.Log(u'开始回滚数据.........')
            oracleSqlList.reverse()
            oraDataHand(self.oracleObjectTwo,oracleSqlList,self._logger)
            self._logger.Log(u'回滚数据成功.........')
    def spliceSql(self,SqlResult):
        #几何 rowid格式化
        geoString=None
        if SqlResult['TO_CHAR(OLD)']:
            OldData=json.loads(SqlResult['TO_CHAR(OLD)'])
        else:OldData={}
        if SqlResult['TO_CHAR(NEW)']:
            NewData=json.loads(SqlResult['TO_CHAR(NEW)'])
            print NewData
            for key in NewData:
                print NewData[key]
        else:NewData={}
        whereDict={};DataDict={};updateDict={}
        if 'GEOMETRY' in OldData or  'GEOMETRY' in NewData:
            if len(OldData)==1 or len(NewData)==1:
                UpdateSql="UPDATE %s SET GEOMETRY=%s %s WHERE %s"
            else:
                UpdateSql="UPDATE %s SET GEOMETRY=%s,%s WHERE %s"
            InsertSql="INSERT INTO %s(GEOMETRY,ROW_ID,%s) VALUES(%s,%s,%s)"
        else:
            UpdateSql="UPDATE %s SET %s WHERE %s"
            InsertSql="INSERT INTO %s(ROW_ID,%s) VALUES(%s,%s)"
        DeleteSql="DELETE FROM %s WHERE %s"
        Param={}
        #坐标转换
        if self.analyzeType:
            whereDict['RAWTOHEX(ROW_ID)']=SqlResult['RAWTOHEX(TB_ROW_ID)']
            if SqlResult['OP_TP']==2:
                updateDict['U_RECORD']=0
                Sql=UpdateSql%(SqlResult['TB_NM'],self.dealColnumForm(2,updateDict),self.dealColnumForm(1,whereDict))
                whereDict=self.whereRowidDealForm(whereDict)
                Param=dict(updateDict.items()+whereDict.items())
            elif SqlResult['OP_TP']==3:
                if 'GEOMETRY' in OldData:
                    geoString=self.geoOrRowidDealForm(0,OldData['GEOMETRY'])
                    OldData.pop('GEOMETRY')
                    updateDict.update(OldData)
                    Sql=UpdateSql%(SqlResult['TB_NM'],geoString,self.dealColnumForm(2,updateDict),self.dealColnumForm(1,whereDict))
                else:
                    updateDict.update(OldData)
                    Sql=UpdateSql%(SqlResult['TB_NM'],self.dealColnumForm(2,updateDict),self.dealColnumForm(1,whereDict))
                whereDict=self.whereRowidDealForm(whereDict)
                if '\"LEVEL\"' in updateDict:
                    updateDict=self.whereLEVELDealForm(updateDict)
                Param=dict(updateDict.items()+whereDict.items())
            elif SqlResult['OP_TP']==1:
                Sql=DeleteSql%(SqlResult['TB_NM'],self.dealColnumForm(1,whereDict))
                whereDict=self.whereRowidDealForm(whereDict)
                Param=dict(whereDict.items())
        else:
            if SqlResult['OP_TP']==2:
                whereDict['RAWTOHEX(ROW_ID)']=SqlResult['RAWTOHEX(TB_ROW_ID)']
                updateDict['U_RECORD']=2
                Sql=UpdateSql%(SqlResult['TB_NM'],self.dealColnumForm(2,updateDict),self.dealColnumForm(1,whereDict))
                whereDict=self.whereRowidDealForm(whereDict)
                Param=dict(updateDict.items()+whereDict.items())
            elif SqlResult['OP_TP']==3:
                whereDict['RAWTOHEX(ROW_ID)']=SqlResult['RAWTOHEX(TB_ROW_ID)']
                if 'GEOMETRY' in NewData:
                    geoString=self.geoOrRowidDealForm(0,NewData['GEOMETRY'])
                    NewData.pop('GEOMETRY')
                    updateDict.update(NewData)
                    if "U_RECORD" not in updateDict:updateDict["U_RECORD"]=3
                    Sql=UpdateSql%(SqlResult['TB_NM'],geoString,self.dealColnumForm(2,updateDict),self.dealColnumForm(1,whereDict))
                else:
                    updateDict.update(NewData)
                    if "U_RECORD" not in updateDict:updateDict["U_RECORD"]=3
                    Sql=UpdateSql%(SqlResult['TB_NM'],self.dealColnumForm(2,updateDict),self.dealColnumForm(1,whereDict))
                whereDict=self.whereRowidDealForm(whereDict)
                if '\"LEVEL\"' in updateDict:
                    updateDict=self.whereLEVELDealForm(updateDict)
                Param=dict(updateDict.items()+whereDict.items())
            elif SqlResult['OP_TP']==1:
                if 'GEOMETRY' in NewData:
                    geoString=self.geoOrRowidDealForm(0,NewData['GEOMETRY'])
                    rowidString=self.geoOrRowidDealForm(1,NewData['ROW_ID'])
                    NewData.pop('GEOMETRY')
                    NewData.pop('ROW_ID')
                    DataDict.update(NewData)
                    DataDict["U_RECORD"]=1
                    Sql=InsertSql%(SqlResult['TB_NM'],self.dealColnumForm(3,DataDict).replace(":",""),geoString,rowidString,self.dealColnumForm(3,DataDict).replace('"LEVEL"','LEVEL1'))
                else:
                    rowidString=self.geoOrRowidDealForm(1,NewData['ROW_ID'])
                    NewData.pop('ROW_ID')
                    DataDict.update(NewData)
                    DataDict["U_RECORD"]=1
                    Sql=InsertSql%(SqlResult['TB_NM'],self.dealColnumForm(3,DataDict).replace(":",""),rowidString,self.dealColnumForm(3,DataDict).replace('"LEVEL"','LEVEL1'))
                if '\"LEVEL\"' in DataDict:
                    DataDict=self.whereLEVELDealForm(DataDict)
                Param=dict(DataDict.items())
        Param=self.formateArrag(Param)
        return Sql,Param
    def formateArrag(self,Param):
        listPoint=None
        for value in Param.values():
            if type(value)==list:
                listPoint=1
                break
        if listPoint:
            for key in Param:
                if type(Param[key])==list:
                    Param[key]=str(Param[key])
        return Param
    #处理rowid参数化
    def whereRowidDealForm(self,whereDict):
        whereDict['ROW_ID']=whereDict['RAWTOHEX(ROW_ID)']
        whereDict.pop('RAWTOHEX(ROW_ID)')
        return whereDict

    #处理LEVEL参数化
    def whereLEVELDealForm(self,whereDict):
        whereDict['LEVEL1']=whereDict['\"LEVEL\"']
        whereDict.pop('\"LEVEL\"')
        return whereDict
    #处理异常字段
    def dealErrColForm(self,key):
        specialField=['RAWTOHEX(ROW_ID)','\"LEVEL\"']
        if key in specialField:
            if key=='RAWTOHEX(ROW_ID)':skey='ROW_ID'
            elif key=='\"LEVEL\"':skey='LEVEL1'
        else:
            skey=key
        return skey
    #字段处理
    def dealColnumForm(self,type,dict):
        stringResultList=[]

        #查询条件格式
        if type==1:
            for key in dict:
                skey=self.dealErrColForm(key)
                whereStrModle="%s=%s"
                stringResultList.append(whereStrModle%(key,":"+skey))
            stringResult=' AND '.join(stringResultList)
        #更新条件格式
        elif type==2:
            for key in dict:
                skey=self.dealErrColForm(key)
                updateStrModle="%s=%s"
                stringResultList.append(updateStrModle%(key,":"+skey))
            stringResult=','.join(stringResultList)
        #新增条件格式
        elif type==3:
            for key in dict:
                stringResultList.append(":"+key)
            stringResult=','.join(stringResultList)
        return stringResult
    #特殊字段转换
    def geoOrRowidDealForm(self,Type,value):
        Result=None
        #几何转换
        if Type==0:
            Geo=wkt2geometry(value)
            Result=geometry2String(Geo)
        #rowid转换
        else:
            Result="HEXTORAW('%s')"%(value)
        return Result
#数据处理
class oraDataHand:
    def __init__(self,oracleObject,oracleSqlList,logger):
        self.oracleObject=oracleObject
        self.oracleSqlList=oracleSqlList
        self._logger=logger
        self.runSql()
    def runSql(self):
        try:
            for Sql in self.oracleSqlList:
                self._logger.Log(u'执行语句：%s %s'%(Sql[0],str(Sql[1])),InfoLevel.INFO_Level)
                print u'执行语句：%s %s'%(Sql[0],str(Sql[1]))
                self.oracleObject.cursor.prepare(Sql[0])
                self.oracleObject.cursor.execute(None,Sql[1])
            #提交事务
            self.oracleObject.conn.commit()
        except Exception as e:
            self._logger.Log(u'执行履历数据构建失败，原因是：%s'%(traceback.format_exc(1)),InfoLevel.ERROR_Level)
            print u'执行履历数据构建失败，原因是：%s'%(traceback.format_exc(1))
            self.oracleObject.conn.rollback()
            exit(1)
#计算GRID坐标点
def grid2geo(grid):
     m1 = int(grid[0:1])
     m2 = int(grid[1:2])
     m3 = int(grid[2:3])
     m4 = int(grid[3:4])
     m5 = int(grid[4:5])
     m6 = int(grid[5:6])
     m7 = int(grid[6:7])
     m8 = int(grid[7:8])
     minx = (m3 * 10 + m4) + (m6 * 450 + m8*450/4.0)/3600 + 60
     miny = ((m1 * 10 + m2) * 2400 + m5 * 300 + m7*300/4)/3600.0
     maxx = minx+0.03125
     maxy = miny+(1.0/(12*4))
     return [minx,miny,maxx,maxy]
#坐标转字符串
def geometry2String(GEOMETRY):
    SDO_GTYPE=str(GEOMETRY.SDO_GTYPE)
    SDO_SRID=str(GEOMETRY.SDO_SRID)
    #node
    if GEOMETRY.SDO_GTYPE==2001:
        SDO_POINT_TYPE='MDSYS.SDO_POINT_TYPE(%s,%s,NULL)'%(str(GEOMETRY.SDO_POINT.X),str(GEOMETRY.SDO_POINT.Y))
        SDO_ELEM_INFO_ARRAY='NULL'
        SDO_ORDINATE_ARRAY='NULL'
    else:
        SDO_POINT_TYPE='NULL'
        SDO_ELEM_INFO_ARRAY='MDSYS.SDO_ELEM_INFO_ARRAY(%s)'%(','.join([str(Point) for Point in GEOMETRY.SDO_ELEM_INFO]))
        SDO_ORDINATE_ARRAY='MDSYS.SDO_ORDINATE_ARRAY(%s)'%(','.join([str(Point) for Point in GEOMETRY.SDO_ORDINATES]))
    GeoStringValue='MDSYS.SDO_GEOMETRY(%s,%s,%s,%s,%s)' %(SDO_GTYPE,SDO_SRID,SDO_POINT_TYPE,SDO_ELEM_INFO_ARRAY,SDO_ORDINATE_ARRAY)
    return GeoStringValue
#wkt转geo
def wkt2geometry(wkt):
    GEOMETRY=struct
    if wkt.startswith('POINT'):
        GEOMETRY.SDO_GTYPE=2001
        GEOMETRY.SDO_SRID=8307
        GEOMETRY.SDO_POINT=struct
        GEOMETRY.SDO_POINT.X=float(wkt.replace("POINT (","").replace(")","").split(" ")[0])
        GEOMETRY.SDO_POINT.Y=float(wkt.replace("POINT (","").replace(")","").split(" ")[1])
        GEOMETRY.SDO_ORDINATES=None
        GEOMETRY.SDO_ELEM_INFO=None
    elif wkt.startswith('LINESTRING'):
        PointList=[]
        GEOMETRY.SDO_GTYPE=2002
        GEOMETRY.SDO_SRID=8307
        GEOMETRY.SDO_POINT=None
        GEOMETRY.SDO_ELEM_INFO=[1,2,1]
        for Point in  wkt.replace("LINESTRING (","").replace(")","").split(", "):
            PointList.extend([float(xy) for xy in Point.split(" ")])
        GEOMETRY.SDO_ORDINATES=PointList
    elif wkt.startswith('POLYGON'):
        PointList=[]
        GEOMETRY.SDO_GTYPE=2003
        GEOMETRY.SDO_SRID=8307
        GEOMETRY.SDO_POINT=None
        GEOMETRY.SDO_ELEM_INFO=[1,1003,1]
        for Point in  wkt.replace("POLYGON ((","").replace("))","").split(", "):
            PointList.extend([float(xy) for xy in Point.split(" ")])
        GEOMETRY.SDO_ORDINATES=PointList
    return GEOMETRY

if __name__=='__main__':
    # Conn={"dbname":"orcl","host":"192.168.4.131","user":"fm_man_sp5_test","passwd":"fm_man_sp5_test","port":"1521"}
    # sql=u'select * from subtask a where  rownum=1'
    # a={'SUBTASK_ID':112}
    Conn={"dbname":"orcl","host":"192.168.4.61","user":"fm_regiondb_test_d_1","passwd":"fm_regiondb_test_d_1","port":"1521"}
    sysConn={"dbname":"orcl","host":"192.168.4.131","user":"LOG_TEST","passwd":"LOG_TEST","port":"1521"}
    Ora=OracleHelper(Conn)
    sysOra=OracleHelper(sysConn)
    LogObject=logDataManage(sysOra,Ora,Conn,60560500,1623,'Test_001')
    #LogObject.inheritLog()#履历继承
    LogObject.structuralData()#数据构建
    #LogObject.rollbackData()#测试数据回滚
    #LogObject.rollbackRegionData()#大区库数据回滚
    #LogObject.cleanLog()#大区库履历清除
    """模型数据构建
    A={"RELATION":{"RD_NODE":{"NODE_PID":0,"CHILD_TABLE":{"RD_LINK":{"LINK_PID":0,"S_NODE_PID":1,"E_NODE_PID":1}}}},
    "GLOBAL_DATA":[{"RD_NODE":{"KIND":1,"ADAS_FLAG":0}},{"RD_LINK":{"KIND":7,"DIRECT":2,"MESH_ID":'605605'}}],
    "DIFFERENCE_DATA":{"RD_NODE":[{"NODE_PID":22920001,"GEO_TEMP":"XY#25","KIND":2},{"NODE_PID":22920002,"GEO_TEMP":"P#25.50"}],
                        "RD_LINK":[{"LINK_PID":22920006,"S_NODE_PID":22920001,"E_NODE_PID":22920002,"GEO_TEMP":"XY#25,Y#25"}]}}

    Conn={"dbname":"orcl","host":"192.168.4.61","user":"fm_regiondb_test_d_1","passwd":"fm_regiondb_test_d_1","port":"1521"}
    Ora=OracleHelper(Conn)
    ConnMongo={"host":"192.168.4.220","port":30000,"dbname":"FastmapSTAF_Unify","tablename":"dddd"}
    Mon=MongodbHelper(ConnMongo)
    RemoveData(Ora,'60560500',A["DIFFERENCE_DATA"].keys())
    run=StructuralOraDataForGDB(Ora,A,'60560500',Mon)
    run.CreateData()
    run.getMemoryData('单RD_LINK线')
    run.MemoryDataForMongo()"""
    # sql=u'select * from RD_LINK A WHERE A.LINK_PID=377440'
    # a={'LINK_PID':22920005,'KIND':10}
    # gemometry=None
    # OracleObject=OracleHelper(Conn)
    # Row=readOracleData(OracleObject,sql)
    # changeKeyWordForOracle(Row)
    # replaceKeyValues(Row,a)
    # #Row.pop('GEOMETRY')
    # LINE=[116.6582, 40.0, 116.6582, 40.000975]
    # GEOMETRY=replaceGeometry(Row['GEOMETRY'],LINE)
    # if 'GEOMETRY' in Row:
    #     gemometry=geometry2String(GEOMETRY)
    #     Row.pop('GEOMETRY')
    # SQL=writeOracleData(Row,gemometry,'RD_LINK')
    # OracleObject.insertData2WithParam(SQL,Row)
    #
    # list='X#50,Y#25'#'XY#25,X#25'#'X#25,Y#25'#'Y#25,X#25'#'XY#1,XY#2,XY#1,X#1,Y#2,XY#4'
    # tt=grid2geo('60560501')
    # point=[tt[0],tt[1]]#[116.625,40.0]
    # AA=CreateGeoData(list)
    # TT=GeoTemp2Geometry(AA.GeoIntermediateData,point)
    # print TT.GeoData









#
#
#
# print aa
# GEOMETRY=struct
# GEOMETRY.SDO_GTYPE=2002
# GEOMETRY.SDO_SRID=8307
# GEOMETRY.SDO_POINT=None
# # GEOMETRY.SDO_POINT.X=None
# # GEOMETRY.SDO_POINT.Y=None
# # GEOMETRY.SDO_POINT.Z=None
# GEOMETRY.SDO_ELEM_INFO=[1.0, 2.0, 1.0]
# GEOMETRY.SDO_ORDINATES=[116.20535, 39.69837, 116.20603, 39.698389999999996, 116.20875, 39.69846, 116.21249, 39.69846, 116.21340000000001, 39.698429999999995]
# # print aa[0]['GEOMETRY'].SDO_GTYPE
# # print aa[0]['GEOMETRY'].SDO_ORDINATES
# # print aa[0]['GEOMETRY'].SDO_ELEM_INFO
# print aa[0]['NAME']
# #OracleObject.cursor.setinputsizes(GEOMETRY=cx_Oracle.OBJECT)
# aa[0]['SUBTASK_ID']=111
# # aa[0]['LINK_PID']=22920000
# # aa[0].pop('ROW_ID')
# MDSYS.SDO_POINT_TYPE
# MDSYS.SDO_ELEM_INFO_ARRAY
# MDSYS.SDO_ORDINATE_ARRAY
# gemometry='MDSYS.SDO_GEOMETRY(2001,8307,MDSYS.SDO_POINT_TYPE(116.36925,39.88714,NULL),NULL,NULL)'
# aa[0].pop('GEOMETRY')
# #print type(aa[0]['GEOMETRY'])
# # aa[0]['\"LEVEL\"']=aa[0]['LEVEL']
# # aa[0].pop('LEVEL')
# #valList=str(aa[0].values()).replace('[','').replace(']','').replace(',',',').replace('None','null')
# colList=str(aa[0].keys()).replace('[',':').replace(']','').replace(',',',:').replace("'","")
# colList0=str(aa[0].keys()).replace('[','').replace(']','').replace("'","")
# #SqL=U'insert into rd_link (%s) values(%s)' %(colList0,colList)
# SqL=u'insert into subtask (GEOMETRY,%s) values(%s,%s)' %(colList0,gemometry,colList)
# print SqL
# print aa[0]
# OracleObject.insertData2WithParam(SqL,aa[0])
#

#清单 4：将任意 Python 对象与游标绑定

# import cx_Oracle
#
# class ArbitraryObject(object):
#
#     def __init__(self, intValue, someOtherData):
#         self.intValue = intValue
#         self.someOtherData = someOtherData
#
#     def BindValue(self):
#         return self.intValue
#
# def InputTypeHandler(cursor, value, numElements):
#     if isinstance(value, ArbitraryObject):
#         return cursor.var(int, arraysize = numElements,
#                 inconverter = ArbitraryObject.BindValue)
#
# connection = cx_Oracle.Connection("cx_Oracle/dev@t11g")
# connection.inputtypehandler = InputTypeHandler
# cursor = connection.cursor()
# cursor.execute("""
#         select *
#         from TestNumbers
#         where IntCol = :obj""",
#         obj = ArbitraryObject(1, "arbitrary"))
# for row in cursor:
#     print "Row:", row
