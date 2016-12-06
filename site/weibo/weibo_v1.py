# -*- coding: utf-8 -*-
__author__ = 'qingfengsheng'

import json
import urllib
import time
import re

from lib.spider import Spider
from lib.util import *

class WeiboV1(Spider):
	"""docstring for WeiboV1"""
	def __init__(selfpath):
		super(Weibo, self).__init__(path)
		print '\n in Weibo __init__'
		if self.config['type'] is "weibo":
			self.before_get_all_weibo()
	# end

	def _get_total_page_v1(self):
		""" 得到需要请求的总次数 """
		if self.config['type'] is "weibo":
			self.get_total_weibo()
	# end

	def _get_params_v1(self, page):
		""" 在发送请求前做一些处理 主要是为了获取参数/数据 """
		if self.config['type'] is "weibo":
			self.get_params_weibo(page)
	# end

	def _check_more_v1(self, text):
		""" 在请求成功返回后做一些处理 主要是为了检查是否还有更多 """
		if self.config['type'] is "weibo":
			self.check_more_weibo(text)
	# end


########################################
# 			用户全部微博			   #
########################################

	def before_get_all_weibo(self):
		self.config['containerid'] =  "100505" + str(self.config['uid']) \
			+ "_-_WEIBO_SECOND_PROFILE_WEIBO"
	# end

	def get_total_weibo(self):
		response = self.simple_request_v1(get_params_weibo(1))
		data = json.loads(response.text)
		return data['cards']['maxPage']
	# end

	def get_params_weibo(self, page):
		params = {
			'containerid': self.config['containerid'],
			'page': page
		}
		return params
	# end

	def check_more_weibo(self, text):
		if text.find('{"mod_type":"mod\/empty"') > 0:
			return False
		else:
			return True
	# end

# end


if __name__ == '__main__':
	weibov1 = WeiboV1('config-v1.ini')
	weibov1.get_date_v1()