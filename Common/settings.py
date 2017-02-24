#!/usr/bin/env python
# -*- coding: utf-8 -*
__author__ = 'wangjun'

import sys, os, re
import time,datetime
import xml.dom.minidom as xdm
reload(sys)
sys.setdefaultencoding('utf-8')

#一体化服务系统库
FM_Man_Conf={"dbname":"orcl","host":"192.168.4.131","user":"fm_man_test","passwd":"fm_man_test","port":"1521"}

#一体化服务sys系统数据
FM_Sys_Conf={"dbname":"orcl","host":"192.168.4.131","user":"fm_sys_test","passwd":"fm_sys_test","port":"1521"}

# 道路履历库信息
LogTestDBConf={"dbname":"orcl","host":"192.168.4.131","user":"LOG_TEST","passwd":"LOG_TEST","port":"1521"}
# 收集服务系统库
IPX_ServerDBConf={"dbname":"orcl","host":"192.168.4.131","user":"IPX_SERVER","passwd":"IPX_SERVER","port":"1521"}
# 输出日志文件名
#logPath = os.path.dirname(os.path.realpath(sys.path[0]))+os.sep+'logs'
logPath = os.path.dirname(os.path.realpath(sys.path[0]))+os.sep+'logs'

if not os.path.exists(logPath):
    os.mkdir(logPath)
log_file = "mining_%s.log" %time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
logfilename = os.path.join(logPath, log_file)

class InfoLevel:
    '''消息'''
    INFO_Level    = 0
    WARNING_Level = 1
    ERROR_Level   = 2
    FAILURE_Level = 3

#执行冒烟测试所需配置文件
ConfFilename =  xdm.parse(re.sub('tactics_drivers','',os.path.abspath(sys.path[0]))+os.sep+'conf'+os.sep+'SmokeConfig.xml').documentElement
# ConfFilename =  xdm.parse(re.sub('runSmoke.exe','',os.path.abspath(sys.path[0]))+'conf'+os.sep+'SmokeConfig.xml').documentElement

InfoRoadEditType={"CREATE:RDLINK":u"创建RDLINK",
                  "UPDATE:RDLINK":u"修改RDLINK",
                  "DELETE:RDLINK":u"删除RDLINK",
                  "BREAK:RDLINK":u"打断RDLINK",
                  "REPAIR:RDLINK":u"修形RDLINK",
                  "DEPART:RDLINK":u"分离RDLINK",
                  "BATCH:RDLINKSPEEDLIMIT":u"批量编辑RDLINKSPEEDLIMIT",
                  "BATCH:RDLINK":u"批量编辑RDLINK",
                  "UPDOWNDEPART:RDLINK":u"上下线分离",
                  "CREATESIDEROAD:RDLINK":u"制作辅路",
                  "CREATE:RDNODE":u"创建RDNODE",
                  "UPDATE:RDNODE":u"修改RDNODE",
                  "DELETE:RDNODE":u"删除RDNODE",
                  "MOVE:RDNODE":u"移动RDNODE",
                  "CREATE:RDRESTRICTION":u"创建交限",
                  "UPDATE:RDRESTRICTION":u"修改交限",
                  "DELETE:RDRESTRICTION":u"删除交限",
                  "CREATE:RDCROSS":u"创建路口",
                  "UPDATE:RDCROSS":u"修改路口",
                  "DELETE:RDCROSS":u"删除路口",
                  "BATCH:RDCROSS":u"编辑路口",
                  "CREATE:RDBRANCH":u"创建分歧",
                  "UPDATE:RDBRANCH":u"修改分歧",
                  "DELETE:RDBRANCH":u"删除分歧",
                  "CREATE:RDLANECONNEXITY":u"创建车信",
                  "UPDATE:RDLANECONNEXITY":u"修改车信",
                  "DELETE:RDLANECONNEXITY":u"删除车信",
                  "CREATE:RDSPEEDLIMIT":u"创建点限速",
                  "UPDATE:RDSPEEDLIMIT":u"修改点限速",
                  "DELETE:RDSPEEDLIMIT":u"删除点限速",
                  "CREATE:RDLINKSPEEDLIMIT":u"创建线限速",
                  "CREATE:ADLINK":u"创建行政区划线",
                  "UPDATE:ADLINK":u"修改行政区划线",
                  "DELETE:ADLINK":u"删除行政区划线",
                  "BREAK:ADLINK":u"打断行政区划线",
                  "REPAIR:ADLINK":u"修形行政区划线",
                  "CREATE:ADNODE":u"创建行政区划点",
                  "UPDATE:ADNODE":u"修改行政区划点",
                  "DELETE:ADNODE":u"删除行政区划点",
                  "MOVE:ADNODE":u"移动行政区划点",
                  "CREATE:ADFACE":u"创建行政区划面",
                  "UPDATE:ADFACE":u"修改行政区划面",
                  "DELETE:ADFACE":u"删除行政区划面",
                  "CREATE:ADADMIN":u"创建行政区划代表点",
                  "UPDATE:ADADMIN":u"修改行政区划代表点",
                  "DELETE:ADADMIN":u"删除行政区划代表点",
                  "MOVE:ADADMIN":u"移动行政区划代表点",
                  "RELATION:ADADMIN":u"行政区划代表点关联面",
                  "UPDATE:ADADMINGROUP":u"修改行政区划层级关系",
                  "CREATE:RWLINK":u"创建RWLINK",
                  "UPDATE:RWLINK":u"修改RWLINK",
                  "DELETE:RWLINK":u"删除RWLINK",
                  "BREAK:RWLINK":u"打断RWLINK",
                  "REPAIR:RWLINK":u"修形RWLINK",
                  "CREATE:RWNODE":u"创建铁路点",
                  "UPDATE:RWNODE":u"修改铁路点",
                  "DELETE:RWNODE":u"删除铁路点",
                  "MOVE:RWNODE":u"移动铁路点",
                  "CREATE:RDGSC":u"创建立交",
                  "UPDATE:RDGSC":u"修改立交",
                  "DELETE:RDGSC":u"删除立交",
                  "CREATE:ZONELINK":u"创建ZONE线",
                  "UPDATE:ZONELINK":u"修改ZONE线",
                  "DELETE:ZONELINK":u"删除ZONE线",
                  "BREAK:ZONELINK":u"打断ZONE线",
                  "REPAIR:ZONELINK":u"修形ZONE线",
                  "CREATE:ZONENODE":u"创建ZONE点",
                  "UPDATE:ZONENODE":u"修改ZONE点",
                  "DELETE:ZONENODE":u"删除ZONE点",
                  "MOVE:ZONENODE":u"移动ZONE点",
                  "CREATE:ZONEFACE":u"创建ZONE面",
                  "UPDATE:ZONEFACE":u"修改ZONE面",
                  "DELETE:ZONEFACE":u"删除ZONE面",
                  "CREATE:LULINK":u"创建土地利用线",
                  "UPDATE:LULINK":u"修改土地利用线",
                  "DELETE:LULINK":u"删除土地利用线",
                  "BREAK:LULINK":u"打断土地利用线",
                  "REPAIR:LULINK":u"修形土地利用线",
                  "CREATE:LUNODE":u"创建土地利用点",
                  "UPDATE:LUNODE":u"修改土地利用点",
                  "DELETE:LUNODE":u"删除土地利用点",
                  "MOVE:LUNODE":u"移动土地利用点",
                  "CREATE:LUFACE":u"创建土地利用面",
                  "UPDATE:LUFACE":u"修改土地利用面",
                  "DELETE:LUFACE":u"删除土地利用面",
                  "CREATE:RDTRAFFICSIGNAL":u"创建交通信号灯",
                  "UPDATE:RDTRAFFICSIGNAL":u"修改交通信号灯",
                  "DELETE:RDTRAFFICSIGNAL":u"删除交通信号灯",
                  "CREATE:RDELECTRONICEYE":u"创建电子眼",
                  "UPDATE:RDELECTRONICEYE":u"修改电子眼",
                  "MOVE:RDELECTRONICEYE":u"移动电子眼",
                  "DELETE:RDELECTRONICEYE":u"删除电子眼",
                  "CREATE:RDELECEYEPAIR":u"创建区间测速电子眼组成",
                  "DELETE:RDELECEYEPAIR":u"删除区间测速电子眼组成",
                  "CREATE:RDWARNINGINFO":u"创建警示信息",
                  "UPDATE:RDWARNINGINFO":u"修改警示信息",
                  "DELETE:RDWARNINGINFO":u"删除警示信息",
                  "CREATE:RDSLOPE":u"创建坡度信息",
                  "UPDATE:RDSLOPE":u"修改坡度信息",
                  "DELETE:RDSLOPE":u"删除坡度信息",
                  "CREATE:RDGATE":u"创建大门信息",
                  "UPDATE:RDGATE":u"修改大门信息",
                  "DELETE:RDGATE":u"删除大门信息",
                  "CREATE:RDSE":u"创建分叉口提示",
                  "UPDATE:RDSE":u"修改分叉口提示",
                  "DELETE:RDSE":u"删除分叉口提示",
                  "CREATE:RDINTER":u"创建CRF交叉点（CRF路口）",
                  "UPDATE:RDINTER":u"修改CRF交叉点（CRF路口）",
                  "DELETE:RDINTER":u"删除CRF交叉点（CRF路口）",
                  "CREATE:LCLINK":u"创建土地覆盖线",
                  "UPDATE:LCLINK":u"修改土地覆盖线",
                  "DELETE:LCLINK":u"删除土地覆盖线",
                  "BREAK:LCLINK":u"打断土地覆盖线",
                  "REPAIR:LCLINK":u"修形土地覆盖线",
                  "CREATE:LCNODE":u"创建土地覆盖点",
                  "UPDATE:LCNODE":u"修改土地覆盖点",
                  "DELETE:LCNODE":u"删除土地覆盖点",
                  "MOVE:LCNODE":u"移动土地覆盖点",
                  "CREATE:LCFACE":u"创建土地覆盖面",
                  "UPDATE:LCFACE":u"修改土地覆盖面",
                  "DELETE:LCFACE":u"删除土地覆盖面",
                  "CREATE:RDSPEEDBUMP":u"创建减速带",
                  "UPDATE:RDSPEEDBUMP":u"修改减速带",
                  "DELETE:RDSPEEDBUMP":u"删除减速带",
                  "CREATE:RDSAMENODE":u"创建同一点",
                  "DELETE:RDSAMENODE":u"删除同一点",
                  "CREATE:RDSAMELINK":u"创建同一线",
                  "DELETE:RDSAMELINK":u"删除同一线",
                  "CREATE:RDDIRECTROUTE":u"创建顺行",
                  "UPDATE:RDDIRECTROUTE":u"修改顺行",
                  "DELETE:RDDIRECTROUTE":u"删除顺行",
                  "CREATE:RDTOLLGATE":u"创建收费站",
                  "UPDATE:RDTOLLGATE":u"修改收费站",
                  "DELETE:RDTOLLGATE":u"删除收费站",
                  "CREATE:RDOBJECT":u"创建CRF对象",
                  "UPDATE:RDOBJECT":u"修改CRF对象",
                  "DELETE:RDOBJECT":u"删除CRF对象",
                  "CREATE:RDVARIABLESPEED":u"创建可变限速",
                  "UPDATE:RDVARIABLESPEED":u"修改可变限速",
                  "DELETE:RDVARIABLESPEED":u"删除可变限速",
                  "CREATE:RDVOICEGUIDE":u"创建语音引导",
                  "UPDATE:RDVOICEGUIDE":u"修改语音引导",
                  "DELETE:RDVOICEGUIDE":u"删除语音引导",
                  "CREATE:RDROAD":u"创建CRF道路",
                  "UPDATE:RDROAD":u"修改CRF道路",
                  "DELETE:RDROAD":u"删除CRF道路",
                  "CREATE:IXSAMEPOI":u"创建POI同一关系",
                  "UPDATE:IXSAMEPOI":u"修改同一POI",
                  "DELETE:IXSAMEPOI":u"删除同一POI",
                  "BATCH:RDLANE":u"批量创建维护删除详细车道信息",
                  "DELETE:RDLANE":u"根据link批量删除详细车道",
                  "BATCH:RDLANETOPODETAIL":u"批量创建维护删除详细车道联通信息",
                  "CREATE:RDHGWGLIMIT":u"创建限高限重",
                  "UPDATE:RDHGWGLIMIT":u"修改限高限重",
                  "MOVE:RDHGWGLIMIT":u"移动限高限重",
                  "DELETE:RDHGWGLIMIT":u"删除限高限重",
                  "CREATE:RDMILEAGEPILE":u"创建里程桩",
                  "UPDATE:RDMILEAGEPILE":u"修改里程桩",
                  "MOVE:RDMILEAGEPILE":u"移动里程桩",
                  "DELETE:RDMILEAGEPILE":u"删除里程桩",
                  "CREATE:RDTMCLOCATION":u"创建TMC匹配",
                  "UPDATE:RDTMCLOCATION":u"修改TMC匹配",
                  "DELETE:RDTMCLOCATION":u"删除TMC匹配"}