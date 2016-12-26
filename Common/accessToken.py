#!/usr/bin/env python
# -*- coding: utf-8 -*
# 用于数据挖掘的公共方法
__author__ = 'wangjun'


#计算tokenAccess

import time
import datetime
import hashlib
#
#  access_token = 48 位字符  -->  简单实现版
#         0~7   : user_id      36位编码,用户id
#         8~15  : time_stamp   36位编码,有效期时间戳
#         16~47 : md5          校验位
#
#         目前可供访问的属性:
#             self.token         access_token
#             self.user_id       用户id
#             self.time_stamp    有效期时间戳
#
#          后续会携带越来越多的信息
#

class AccessToken:

    # 10进制转36进制对照表
    __table_d2n = {   0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9',
                     10: 'A',11: 'B',12: 'C',13: 'D',14: 'E',15: 'F',16: 'G',17: 'H',18: 'I',19: 'J',
                     20: 'K',21: 'L',22: 'M',23: 'N',24: 'O',25: 'P',26: 'Q',27: 'R',28: 'S',29: 'T',
                     30: 'U',31: 'V',32: 'W',33: 'X',34: 'Y',35: 'Z' }

    # 36进制转10进制对照表
    __table_n2d = {  '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
                     'A': 10,'B': 11,'C': 12,'D': 13,'E': 14,'F': 15,'G': 16,'H': 17,'I': 18,'J': 19,
                     'K': 20,'L': 21,'M': 22,'N': 23,'O': 24,'P': 25,'Q': 26,'R': 27,'S': 28,'T': 29,
                     'U': 30,'V': 31,'W': 32,'X': 33,'Y': 34,'Z': 35 }

    def __init__(self, token = None):
        """ 初始化，如果传入的token不为空，即刻开始token的分裂解析"""
        self.token = token
        if self.token is not None:
            self.user_id = self.__n2d(self.token[0:8])
            self.time_stamp = self.__n2d(self.token[8:16])

    def generate(self, user_id, expire_seconds=86400):
        """ 根据user_id生成一个token
            expire_seconds : 该token的过期日期，从生成的时间开始计算，单位：秒
            86400表示一天的有效期
            @todo: 后续会携带越来越多的信息
        """
        # 成员赋值
        self.user_id = user_id
        self.time_stamp = int(time.mktime((datetime.datetime.now() + datetime.timedelta(seconds = expire_seconds)).timetuple()))
        # 计算组装token
        userId = self.__d2n(self.user_id).rjust(8, '0')

        timestamp = self.__d2n(self.time_stamp).ljust(8, '0')
        hash=hashlib.md5()
        hash.update(userId+timestamp)
        md5 = hash.hexdigest().upper()
        self.token = (userId + timestamp + md5)
        return self.token
    def Token2UserID(self,token):
        #token计算用户ID
        userId=None
        try:
            userString=token[0:8]
            userId=self.__n2d(userString)
        except Exception,e:
            print e
        return userId
    # def availability(self):
    #     """ token是否合法
    #         @return  -1  非法token
    #                  -2  已过有效期
    #                  0   合法
    #     """
    #     try:
    #         if self.token==None or self.token.__len__()<48:
    #             return Static_con.token_error
    #         userId = self.__d2n(self.user_id).rjust(8, '0')
    #         timestamp = self.__d2n(self.time_stamp).rjust(8, '0')
    #         hash=hashlib.md5()
    #         hash.update(userId+timestamp)
    #         md5 = hash.hexdigest().upper()
    #         if md5 != self.token[16:48]:
    #             return Static_con.token_error
    #         if self.time_stamp < time.time():
    #             return Static_con.token_expired
    #         return Static_con.token_right
    #     except Exception,e:
    #         print e
    #         return Static_con.token_expired

    def __d2n(self, d):
        """10进制转换36进制"""
        result = []
        div, mod = divmod(d, 36)
        result.append(AccessToken.__table_d2n[mod])
        while div >= 36:
            div, mod = divmod(div, 36)
            result.append(AccessToken.__table_d2n[mod])
        result.append(AccessToken.__table_d2n[div])
        result.reverse()
        return ''.join(result)

    def __n2d(self, n):
        """36进制转换10进制"""
        #0000016J
        try:
            array = list(str(n).lstrip('0'))
            array.reverse()
            result = 0
            for i, x in enumerate(array):
                result += AccessToken.__table_n2d[x] * (36 ** i)
            return result
        except Exception,e:
            print e
            return 0

if __name__=="__main__":

    token = AccessToken()
    tokenStr=token.generate(1623, 172800)
    print tokenStr
    print token.Token2UserID(tokenStr)
    # token = AccessToken("000009D200ND9M7E20825D409DE6CA00004AEA68FE4FB581")
    # print token.user_id
    # type=token.availability()
    #
    # token = AccessToken()
    # token.generate(59, 86400)
    # type=token.availability()
    # print tokenStr
    # print type



