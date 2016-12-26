#!/usr/bin/env python
# -*- coding: utf-8 -*
# 用于数据挖掘的公共方法
__author__ = 'wangjun'

# {"errmsg":"success",
#  "data":{
#      "log":
#          [{"type":"RDLINK","pid":510000579,"childPid":"","op":"淇敼"},
#           {"type":"RDGSCLINK","pid":407000006,"childPid":"","op":"淇敼"}],
#      "check":[],
#      "pid":510000579},"errcode":0}

def replaceIntForDict(dictObject):
    for key in dictObject:
        if isinstance(dictObject[key], int):
            dictObject[key] = 0
        elif isinstance(dictObject[key], dict):
            replaceIntForDict(dictObject[key])
        elif isinstance(dictObject[key], list):
            replaceIntForList(dictObject[key])
    return dictObject

def replaceIntForList(listObject):
    count = 0
    for item in listObject:
        if isinstance(item, int):
            listObject[count] = 0
        elif isinstance(item, dict):
            listObject[count] = replaceIntForDict(listObject[count])
        elif isinstance(item, list):
            listObject[count] = replaceIntForList(listObject[count])
        count += 1
    return listObject

# a={"errmsg":None,"data":{"log":[{"type":"RDNODE","pid":502000731,"childPid":"","op":"新增"},{"type":"RDNODE","pid":501000744,"childPid":"","op":"新增"},{"type":"RDLINK","pid":505000935,"childPid":"","op":"新增"},{"type":"RDLANE","pid":420000366,"childPid":"","op":"新增"},{"type":"RDLANE","pid":508000359,"childPid":"","op":"新增"}],"check":[],"pid":505000935},"errcode":-1}
# b = {"errmsg":"查询的PID为：420000859的RD_LINK不存在","data":None,"errcode":-1}
#
# if __name__ == '__main__':
#     from oracleUtil import OracleHelper
#     from logger import logger
#     from settings import *
#     import json
#     Logger = logger(logfilename)
#     conn = {"dbname":"orcl","host":"192.168.4.131","user":"LOG_TEST","passwd":"LOG_TEST","port":"1521"}
#     oracleObject = OracleHelper(conn, Logger)
#     api_sql="SELECT ID,TO_CHAR(REQ) AS REQ,TO_CHAR(ACK) AS ACK,TYPE FROM strategy_edit_fast_regression l WHERE l.c_id='test'"
#     runList = oracleObject.executeSQL(api_sql)
#     for temp in runList:
#         temp1 = eval(json.loads(temp["ACK"]))
#         p=replaceIntForDict(temp1)
#         print p
