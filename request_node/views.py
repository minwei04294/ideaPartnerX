# Create your views here.
#-*- coding:utf8 -*-
import json,traceback
from Common.commonUtil import getParamFromRequest
from Common.response import sucResponse
from Work_Common.accessToken import AccessToken
from Common.logger import logger
from Common.settings import *

def testStart(request):
    Logger=logger(logPath+os.sep+'IdeaParterServerLog')
    tokenObj=AccessToken()
    TokenCode=getParamFromRequest(request,'access_token')
    Token=tokenObj.Token2UserID(TokenCode)
    Logger.Log(u"开始执行测试打点:用户ID:%s"%Token)
    queryResult=[]
    return sucResponse(queryResult)
def testStop(request):
    Logger=logger(logPath+os.sep+'IdeaParterServerLog')
    tokenObj=AccessToken()
    TokenCode=getParamFromRequest(request,'access_token')
    Token=tokenObj.Token2UserID(TokenCode)
    Logger.Log(u"结束执行测试打点:用户ID:%s"%Token)
    queryResult=[]
    return sucResponse(queryResult)