#!/usr/bin/env python
# -*- coding: utf-8 -*

__author__ = 'ZQ'

import sys, re, traceback
from Common.logger import logger
from Common.settings import *
from Common.oracleUtil import OracleHelper
from EditFastRegressionDriver import *

reload(sys)
sys.setdefaultencoding('utf-8')

class SmokeRunner(object):
    def __init__(self, dbid, userid, mode, conn, logger):
        self._logger = logger
        self._dbid = dbid
        self._userid = int(userid)
        self._mode = mode
        self.oracleObject=OracleHelper(conn, logger)
    #获取测试集合对应的请求总数
    def GetTestCase(self, case_name):
        try:
            sql = "SELECT COUNT(1) FROM strategy_edit_fast_regression l WHERE l.c_id='{0}'".format(case_name)
            case_count = self.oracleObject.selectData(sql)
        except Exception:
            self._logger.Log(u"执行获取测试集合对应的请求总数失败：%s" % traceback.format_exc(), InfoLevel.ERROR_Level)
            raise Exception
        return case_count
    #替换logid
    def replacelogid(self, target, where):
        try:
            sql = "UPDATE STRATEGY_EDIT_FAST_REGRESSION SET LOG_ID = :1 WHERE %s" % where
            self.oracleObject.changeData2WithParam(sql, [target])
            self.oracleObject.commitData()
        except Exception:
            self._logger.Log(u"执行替换logid失败：%s" % traceback.format_exc(), InfoLevel.ERROR_Level)
            raise Exception
    #筛选有效logid
    def GetExecutLogid(self):
        logidlist = []
        try:
            #取消logid的显示和替换，改为执行输入logids
            # sql = "SELECT DISTINCT L.\"DESCP\", L.LOG_ID FROM strategy_edit_fast_regression l WHERE l.c_id='{0}'".format(case_name)
            # while 1:
            #     #提示用户替换logid
            #     logids = self.oracleObject.selectData(sql)
            #     self._logger.Log(u"测试集合【%s】对应的测试数据集id如下：" % (case_name), InfoLevel.INFO_Level)
            #     for logs in logids:
            #         # print logs["DESCP"],logs["LOG_ID"]
            #         self._logger.Log(u"【%s】 ：【%s】 " % (logs["DESCP"],logs["LOG_ID"]), InfoLevel.INFO_Level)
            #     self._logger.Log(u"是否需要替换测试数据集id？ Y/N", InfoLevel.INFO_Level)
            #     choose = raw_input()
            #     if choose == 'Y' or choose == 'y':
            #         self._logger.Log(u"请输入正确的测试数据集id及where条件，英文逗号','隔开。多组替换条件用半角分号';'隔开", InfoLevel.INFO_Level)
            #         logidpars = raw_input().decode('gbk').encode('utf-8').split(';')
            #         # logidpars = raw_input().split(';')
            #         for pars in logidpars:
            #             params = pars.split(',')
            #             self.replacelogid(params[0], params[1])
            #     elif choose == 'N' or choose == 'n' :
            #         break
            #筛选有效logid
            # for logid in logids:
            #     if not (logid["LOG_ID"] == 'error:Non find information' or logid["LOG_ID"] == '数据集ID不唯一' or logid["LOG_ID"] is None):
            #         if logid["LOG_ID"] not in logidlist:
            #             logidlist.append(logid["LOG_ID"])
            if self._mode == SmokeMode.Run_Feature:
            #如果按要素执行，需要人为输入logids
                self._logger.Log(u"请输入所需的测试数据集id，多个用英文逗号','隔开", InfoLevel.INFO_Level)
                logids = raw_input().replace(' ','')
                if not logids:
                    self._logger.Log(u"未输入任何测试数据集id，请再次确认！", InfoLevel.INFO_Level)
                else:
                    for logid in logids.split(','):
                        sql = "SELECT * FROM LOG_DETAIL L WHERE L.DATA_SET_ID = '{0}'".format(logid)
                        num = self.oracleObject.selectData(sql)
                        if not num:
                            self._logger.Log(u"测试数据集id【%s】未找到，请再次确认！" % logid, InfoLevel.INFO_Level)
                        else:
                            logidlist.append(logid)
            elif self._mode == SmokeMode.Run_All:
            #如果全量执行，则logids为strategy全表的logid
                sql = "SELECT DISTINCT L.LOG_ID FROM strategy_edit_fast_regression l"
                logids = self.oracleObject.selectData(sql)
                for logid in logids:
                    if not (logid["LOG_ID"] == 'error:Non find information' or logid["LOG_ID"] == '数据集ID不唯一' or logid["LOG_ID"] is None):
                        if logid["LOG_ID"] not in logidlist:
                            logidlist.append(logid["LOG_ID"])
        except Exception:
            self._logger.Log(u"执行筛选有效logid失败：%s" % traceback.format_exc(), InfoLevel.ERROR_Level)
            raise Exception
        return logidlist

    #获取请求的执行结果
    def GetResultCount(self, case_name):
        SucCount = FailCount = SkipCount = 0
        try:
            if self._mode == SmokeMode.Run_Feature:
                sql = "SELECT L.REQ_RESULT RR, L.SQLS_RESULT SR FROM strategy_edit_fast_regression l WHERE l.c_id='{0}'".format(case_name)
            elif self._mode == SmokeMode.Run_All:
                sql = "SELECT L.REQ_RESULT RR, L.SQLS_RESULT SR FROM strategy_edit_fast_regression l"
            ResultCount = self.oracleObject.selectData(sql)
            for Result in ResultCount:
                if Result["RR"] == 'Pass' and Result["SR"] == 'Pass': SucCount += 1
                elif Result["RR"] == 'Pass' and not Result["SR"] == 'Pass': FailCount +=1
                elif Result["RR"] == 'Failed' : FailCount +=1
                else: SkipCount +=1
        except Exception:
            self._logger.Log(u"执行获取请求执行结果失败：%s" % traceback.format_exc(), InfoLevel.ERROR_Level)
            raise Exception
        return SucCount, FailCount, SkipCount
    #执行请求
    def RunTestCase(self, case_name):
        assert(case_name)
        EFR = EditFastRegression(LogTestDBConf, self._logger)
        #构建数据
        # logidlist = self.GetExecutLogid(case_name)
        logidlist = self.GetExecutLogid()
        if logidlist:
            for log1 in logidlist:
                self._logger.Log(u"测试数据集id【%s】构建数据开始：" % log1, InfoLevel.INFO_Level)
                EFR.bulidTestDataByLog(self._dbid, self._userid, log1)
                self._logger.Log(u"测试数据集id【%s】构建数据完成。" % log1, InfoLevel.INFO_Level)
        #执行请求并验证
        self._logger.Log(u"执行并验证请求开始：", InfoLevel.INFO_Level)
        #获取待执行的请求
        if self._mode == SmokeMode.Run_Feature:
            api_sql = "SELECT ID,TO_CHAR(REQ) AS REQ,TO_CHAR(ACK) AS ACK,TYPE FROM strategy_edit_fast_regression l WHERE l.c_id='{0}'"
        elif self._mode == SmokeMode.Run_All:
            api_sql = "SELECT ID,TO_CHAR(REQ) AS REQ,TO_CHAR(ACK) AS ACK,TYPE FROM strategy_edit_fast_regression l"
        runList = self.oracleObject.selectData(api_sql.format(case_name))
        newToken = EFR.getUser2Token(self._userid)
        for temp in runList:
            #替换token
            oldToken = re.findall(r'.*access_token=(.*)&', str(temp['REQ']))[0]
            temp["REQ"] = EFR.replaceData(temp["REQ"], oldToken, newToken)
            #测试验证
            tp=json.loads(json.loads(temp['ACK']))
            EFR.replayHttp(temp["REQ"], tp, temp["TYPE"], temp["ID"])
        self._logger.Log(u"执行并验证请求完成。", InfoLevel.INFO_Level)
        #统计执行结果
        TotalCount = len(runList)
        SucCount, FailCount, SkipCount = self.GetResultCount(case_name)
        #回滚大区库
        if not logidlist:
            EFR.rollbackDataByLog(self._dbid, self._userid, '')
        else:
            for log2 in logidlist:
                self._logger.Log(u"测试数据集id【%s】回滚大区库数据+回滚构建数据开始：" % log2, InfoLevel.INFO_Level)
                EFR.rollbackDataByLog(self._dbid, self._userid, log2)
                self._logger.Log(u"测试数据集id【%s】回滚大区库数据+回滚构建数据完成。" % log2, InfoLevel.INFO_Level)

        return TotalCount, SucCount, FailCount, SkipCount
    #执行冒烟测试
    def run(self, case_list):
        self._logger.Log(u"="*60)
        self._logger.Log(u"冒烟测试执行开始",InfoLevel.INFO_Level)
        execCaseList = []
        total_case_count = suc_case_count = fail_case_count = skip_case_count = 0
        iTotalApiCount = iSucApiCount = iFailApiCount = iSkipApiCount = 0
        for casename in case_list:
            testcaseCount = self.GetTestCase(casename)[0]["COUNT(1)"]
            total_case_count += 1
            if not testcaseCount:
                self._logger.Log(u"用例库中未找到测试集合【%s】，请再次确认！" % casename, InfoLevel.ERROR_Level)
                skip_case_count +=1
            elif testcaseCount == '0':
                self._logger.Log(u"测试集合【%s】无对应的有效接口请求，请再次确认！" % casename, InfoLevel.ERROR_Level)
                fail_case_count += 1
            else :
                execCaseList.append(casename)
        if not execCaseList:
            self._logger.Log(u"待执行的测试集合，均不符合执行条件，请核对后重新执行！", InfoLevel.ERROR_Level)
        else:
            for testCase in execCaseList:
                # 执行测试集合
                self._logger.Log(u"测试集合【%s】执行开始：" % testCase, InfoLevel.INFO_Level)
                try:
                    iTotalApiCount, iSucApiCount, iFailApiCount, iSkipApiCount = self.RunTestCase(testCase)
                except Exception:
                    self._logger.Log(u"执行测试集合失败：%s" % traceback.format_exc(), InfoLevel.INFO_Level)
                self._logger.Log(u"测试集合【%s】执行结束，需要执行【%d】个接口请求，其中成功：【%d】，失败：【%d】，未执行：【%d】"
                                 %(testCase, iTotalApiCount, iSucApiCount, iFailApiCount, iSkipApiCount), InfoLevel.INFO_Level)
                if iFailApiCount > 0 or iSkipApiCount > 0 :
                    fail_case_count += 1
                elif iSucApiCount > 0 :
                    suc_case_count += 1
        self._logger.Log(u"冒烟测试执行结束，共有【%d】个测试集合，执行了【%d】个测试集合，其中成功:【%d】，失败:【%d】，未找到:【%d】"
                         %(total_case_count, total_case_count-skip_case_count, suc_case_count, fail_case_count, skip_case_count), InfoLevel.INFO_Level)
        self._logger.Log(u"="*60)

if __name__ == '__main__':
    Logger = logger(logfilename)
    s = SmokeRunner(257, 3680, SmokeMode.Run_All, LogTestDBConf, Logger)
    SucCount, FailCount, SkipCount =s.GetResultCount('test')
    print SucCount, FailCount, SkipCount, SucCount+FailCount+SkipCount