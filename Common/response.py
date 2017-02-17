#-*- coding:utf8 -*-
from django.http import HttpResponse
import json
from Common.modelsEncoder import DateEncoder

class errResponse(HttpResponse):
	def __init__(self,errmsg,errcode=-1,dataList=None):
		response_data = {}
		response_data['errcode'] = errcode
		response_data['data'] = dataList
		print type(errmsg)
		if 'unicode'==type(errmsg).__name__.lower():
			response_data['errmsg'] = errmsg
		else:
			response_data['errmsg'] = str(errmsg)
		super(errResponse, self).__init__(
            content = json.dumps(response_data,ensure_ascii=False,cls=DateEncoder),
            content_type = 'application/json',
        )
		#	跨域访问设置
		self['Access-Control-Allow-Origin'] = '*'
		self['Access-Control-Allow-Methods'] = 'POST,GET,OPTIONS,DELETE,PUT'
		
class sucResponse(HttpResponse):
	def __init__(self, dataList = None):		
		data = {}
		data['errcode'] = 0
		data['errmsg'] = "success"
		data['data'] = dataList
		super(sucResponse, self).__init__(
            content = json.dumps(data,ensure_ascii=False,cls=DateEncoder),
            content_type = 'application/json',
        )
		#	跨域访问设置
		self['Access-Control-Allow-Origin'] = '*'
		self['Access-Control-Allow-Methods'] = 'POST,GET,OPTIONS,DELETE,PUT'