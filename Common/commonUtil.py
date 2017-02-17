#__author__ = 'zhangxiaoyi'
#-*- coding:utf8 -*-


from BaseHTTPServer import BaseHTTPRequestHandler


def getParamFromRequest(request,parameterName):
        if request.method == 'GET':
            try:
                return  request.GET[parameterName]
            except Exception,e: print e
        elif request.method == 'POST':
            try:
                return  request.POST[parameterName]
            except Exception,e: print e
        return None
def getFileFromRequest(request,parameterName):
    if request.method == 'GET':
            raise Exception("文件上传不能采用get方式")
    if request.method == 'POST':
        try:
            return  request.FILES[parameterName]
        except Exception,e: print e
    return None

'''
     * 根据ids构造字符串
     * ids=1,2,3,4,5,6,7
     * column=taskUuid
     * return=taskUuid in ('1','2','3','4') or taskUuid in ('5','6','7')
     * @param ids
     * @param column
     * @return
'''
def makeSqlByString(idlist,column):
    returnStr=column+" in("
    if idlist is None or idlist.__len__()==0:
        return None
    conditionStr=""
    for i in range(0,idlist.__len__()):
        print idlist[i]
    	if ((i+1)%10==0 and i!=idlist.__len__()-1):
    		if conditionStr.rfind(",")!=-1:
    			conditionStr=conditionStr[0: conditionStr.rfind(",")]
    		conditionStr+=" ) or "+column+" in("
    	conditionStr+="'"+str(idlist[i])+"',"

    if(conditionStr.rfind(",")!=-1):
        conditionStr=conditionStr[0:conditionStr.rfind(",")]
    conditionStr=conditionStr+")"
    returnStr=returnStr+conditionStr
    return returnStr

def descException(classException):
    if isinstance(classException,TypeError):
        return u"变量类型错误异常!"
    else:
        return u"未知异常，请联系研发负责人!"

def cursorToList(dataCursor):
    return list(dataCursor)
# 	retList = []
# 	for item in dataCursor:
# 		retList.append(item)
# 	return retList
def _navHash(val):
    return (0 if (val is None )else  hash(val))
if __name__=="__main__":
    idlist=[1,2,3,4,5,6,7,8]
    print makeSqlByString(idlist,"id")