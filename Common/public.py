#!/usr/bin/env python
# -*- coding: utf-8 -*
# 用于数据挖掘的公共方法
__author__ = 'wangjun'

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

def replaceAddPidForDict(dictObject):
    for key in dictObject:
        if key == 'data' and isinstance(dictObject[key], dict):
            dictObject[key]['pid'] = 0
        if key == 'op' and dictObject[key] == u"新增":
            replaceIntForDict(dictObject)
        elif isinstance(dictObject[key], dict):
            replaceAddPidForDict(dictObject[key])
        elif isinstance(dictObject[key], list):
            replaceAddPidForList(dictObject[key])
    return dictObject

def replaceAddPidForList(listObject):
    count = 0
    for item in listObject:
        if isinstance(item, dict):
            listObject[count] = replaceAddPidForDict(listObject[count])
        elif isinstance(item, list):
            listObject[count] = replaceAddPidForList(listObject[count])
        count += 1
    return listObject

# if __name__ == '__main__':
#     a = {"errmsg":None,"data":{"log":[{"type":"RDNODE","pid":502000731,"childPid":502000731,"op":u"新增"},{"type":"RDNODE","pid":501000744,"childPid":501000744,"op":u"修改"},{"type":"RDLINK","pid":505000935,"childPid":505000935,"op":u"删除"},{"type":"RDLANE","pid":420000366,"childPid":"","op":u"新增"},{"type":"RDLANE","pid":508000359,"childPid":"","op":u"新增"}],"check":[],"pid":505000935},"errcode":-1}
#     b = {"errmsg":u"查询的PID为：420000859的RD_LINK不存在","data":None,"errcode":-1}
#     c = {"errmsg":"success","data":{"result":{u"删除link删除信号灯":[{"objType":"RDTRAFFICSIGNAL","pid":505000022,"status":"DELETE"}],u"删除link删除详细车道":[{"objType":"RDLANE","pid":409000349,"status":"DELETE"},{"objType":"RDLANE","pid":405000336,"status":"DELETE"}],u"删除Link":[{"objType":"RDLINK","pid":406000864,"status":"DELETE"}],u"删除Node":[{"objType":"RDNODE","pid":404000622,"status":"DELETE"}]},"log":[],"check":[],"pid":0},"errcode":999}
#     print replaceAddPidForDict(a)