#__author__ = 'zhangxiaoyi'
#-*- coding:utf8 -*-
import json
from datetime import datetime

class DateEncoder(json.JSONEncoder ):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.__str__()
        return json.JSONEncoder.default(self, obj)