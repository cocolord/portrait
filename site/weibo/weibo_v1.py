# -*- coding: utf-8 -*-
__author__ = 'qingfengsheng'

import json
import urllib
import time
import re
from pyquery import PyQuery as pq

from lib.spider import Spider
from lib.util import *

class WeiboV1(Spider):
	"""docstring for WeiboV1"""
	def __init__(self, path):
		super(WeiboV1, self).__init__(path)
		print '\n in WeiboV1 __init__'
		if self.config['type'] == "weibo":
			self.before_get_all_weibo()
	# end

	def _get_total_page_v1(self):
		""" 得到需要请求的总次数 """
		if self.config['type'] == "weibo":
			pages = self.get_total_weibo()
		elif self.config['type'] == "weibo-wap":
			pages = self.get_total_weibo_wap()
		return pages
	# end

	def _get_params_v1(self, page):
		""" 在发送请求前做一些处理 主要是为了获取参数/数据 """
		if self.config['type'] == "weibo":
			params = self.get_params_weibo(page)
		elif self.config['type'] == "weibo-wap":
			params = self.get_params_weibo_wap(page)
		return params
	# end

	def _check_more_v1(self, text):
		""" 在请求成功返回后做一些处理 主要是为了检查是否还有更多 """
		if self.config['type'] == "weibo":
			more = self.check_more_weibo(text)
		elif self.config['type'] == "weibo-wap":
			more = self.check_more_weibo_wap(text)
		return more
	# end


	########################################
	# 			用户全部微博			   #
	########################################

	def before_get_all_weibo(self):
		self.config['containerid'] =  "100505" + str(self.config['uid']) \
			+ "_-_WEIBO_SECOND_PROFILE_WEIBO"
	# end

	def get_total_weibo(self):
		url = self.config['base_url']
		header = self._get_header_v1()
		response = self.simple_request_v1(url, header, self.get_params_weibo(1))
		try:
			data = json.loads(response.text)
		except Exception as e:
			print "Tip: please check cookie"
			print response.text
			raise
		print data['cards'][0]['maxPage']
		return data['cards'][0]['maxPage']
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

	########################################
	#   	wap 版用户全部微博			   #
	########################################

	def get_total_weibo_wap(self):
		# document.querySelector('input[name="mp"]').value
		url = self.config['base_url']
		header = self._get_header_v1()
		response = self.simple_request_v1(url, header, self.get_params_weibo(1))

		# return 6835

	def get_params_weibo_wap(self, page):
		return {
			'page': page
		}

	def check_more_weibo_wap(self, text):
		""" wap 版一开始就确定了总页数 """
		return True

# end


if __name__ == '__main__':
	weibov1 = WeiboV1('config-v1.ini')
	weibov1.get_data_v1(worker=20)