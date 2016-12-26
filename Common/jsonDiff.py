#!/usr/bin/env python
# -*- coding: utf-8 -*
# 用于数据挖掘的公共方法
__author__ = 'wangjun'

from copy import deepcopy

def jsonDiffValue(key, expectVal, actualVal):
    '''对比值'''
    outLog = None
    if (expectVal and not actualVal) or (not expectVal and actualVal):
        outLog = {key:{'expect':expectVal, 'actual':actualVal}}
    elif (not expectVal and not actualVal):
        return outLog
    else:
        if type(expectVal) == list:
            diffVal = []
            firstVal = expectVal[0]
            newActualVal = deepcopy(actualVal)
            # 首先过滤掉明显不需要的字段
            if type(firstVal) == dict:
                for item in newActualVal:
                    bakitem = deepcopy(item)
                    for actualKey in bakitem:
                        if actualKey not in firstVal:
                            del item[actualKey]
            else:
                if type(expectVal[0]) == dict:
                    diffVal = [x for x in expectVal if 'exists' not in x and  x not in newActualVal] + \
                    [x for x in expectVal if 'exists' in x and x['exists'] and x not in newActualVal] + \
                    [x for x in expectVal if 'exists' in x and (not x['exists']) and x in newActualVal]
                else: diffVal = [x for x in expectVal if x not in newActualVal]
            if diffVal:
                outLog = {key:{'expect':expectVal, 'actual':actualVal}}
        elif type(expectVal) == dict:
            outLogTemp={}
            for feild in expectVal:
                outLog1 = jsonDiffValue(feild, expectVal[feild], actualVal[feild])
                if type(outLog1)==dict:
                    outLogTemp.update(outLog1)
            outLog=outLogTemp
        else:
            if expectVal != actualVal:
                outLog = {key:{'expect':expectVal, 'actual':actualVal}}
    return outLog

def verifyData(expectdata, actualdata):
    '''对比验证预期值和实测值'''
    assert(expectdata)
    assert(actualdata)
    retDiffResult = []
    for key in expectdata:
        diffResult = {}
        if key not in actualdata:
            diffResult[key] = {'expect':'exists','actual':'not find'}
        else:
            diffResult = jsonDiffValue(key, expectdata[key], actualdata[key])
        if diffResult: retDiffResult.append(diffResult)
    return retDiffResult