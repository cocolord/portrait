# -*- coding: utf-8 -*-
__author__ = 'qingfengsheng'

import requests
import thread
import threading
import time
import math
import random

import util


class Spider(object):
	"""
	- 以'_'开头的方法均需要子类根据自身情况实现，实例无须调用，无意义
	- 以字母开头的方法是由实例调用的
	"""

	def __init__(self, path="./config.ini"):
		"""
		检查配置文件是否存在，不存在则直接return
		检查输出文件夹是否存在，不存在则创建
		config.ini必须要有的字段
			- dump_dir
			- base_url
		"""
		print u'\n in Spider __init__'
		if not util.check_file(path):
			print '\n\t no file ' + path
			return
		self.config = util.init(path)
		if self.config.has_key('ua'):
			self.config['ua'] = util.init(self.config['ua'])
		self.config['requests_dir'] = self.config['dump_dir'] + '/requests'
		print self.config
		util.check_path(self.config['dump_dir'])
	# end __init__

	def _get_params(self, index, page):
		""" 拼接 url 请求参数 """
		pass
	# end _get_params

	def _check_more(self, text):
		""" 检查是否服务器繁忙，是否登录，是否还有更多数据
		@return Bool <True> 有
		@return Bool <False> 无
		"""
		pass
	# end _check_more

	def _filter(self, text):
		""" 因数据而已，需要返回格式化后的文本数据 """
		pass
	# end _filter

	def get_data(self):
		""" 抓取数据
		如果响应成功：检查是否需要继续请求，存储response文本
		如果响应失败：次数超过10次，直接退出

		Note：返回false不一定就没有更多，可能服务器繁忙
		"""
		fail = 0 		# 请求失败次数
		index = 0 		# 已经加载的数据个数
		page = 1 		# 请求次数
		more = True 	# 循环条件，初始为 True
		header = {
			'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'
		}
		if not self.config.has_key('cookie'):
			self.config['cookie'] = ""
		header['Cookie'] = self.config['cookie']

		while more:
			print '\n no.' + str(page)
			params = self._get_params(index, page)
			if self.config.has_key('type') and self.config['type'] == 'post':
				url = self.config['base_url']
				response = requests.post(url, data=params, headers=header)
			else:
				url = self.config['base_url'] + params
				response = requests.get(url, headers=header)
			print '\t\t status: ' + str(response.status_code)
			if response.status_code == 200:
				util.output(self.config['requests_dir'], page, response.text)
				more = self._check_more(response.text)
				print '\t\t\t has_more: ' + str(more)
				if more is False and fail < 10:
					more = True
					fail += 1
					print '\n\tfail: ' + str(fail) + '\ttry again'
				else:
					fail = 0
					page += 1
					index += 10
			else:
				if fail > 10:
					break
				fail += 1
				print '\n\t\t something wrong, fail ' + str(fail) + '\n\n'
			print '\n'
	# end get_data

	def extract(self):
		""" 提取有效数据 """
		print '\n\t in extract'
		files = util.get_dir_list(self.config['requests_dir'])
		output_path = self.config['dump_dir']
		util.check_path(output_path)
		files.sort(key=lambda x:int(x[:-4]))
		content = ""
		for file in files:
			path = self.config['requests_dir'] + '/' + file
			f = open(path)
			text = f.readlines()
			f.close()
			print path
			content += self._filter(text)
		util.output(output_path, 'total', content)
	# end extract

##############################################################################
##############################################################################
##############################################################################

	def _get_total_page_v1(self):
		""" 得到需要请求的总次数 """
		pass
	# end

	def _get_params_v1(self, page):
		""" 在发送请求前做一些处理 主要是为了获取参数/数据 """
		pass
	# end

	def _check_more_v1(self, text):
		""" 在请求成功返回后做一些处理 主要是为了检查是否还有更多 """
		pass
	# end

	def _get_header_v1(self, index=""):
		""" 随机分配一个请求头，主要是 UA 和 Cookie """
		if index == "":
			key = int(math.floor(random.random()*33))
		else:
			key = index
		if 'cookie' not in self.config:
			self.config['cookie'] = ""
		if 'authorization' not in self.config:
			self.config['authorization'] = ""
		header = {
			'User-Agent': self.config['ua'][key],
			'Cookie': self.config['cookie'],
			'authorization': self.config['authorization']
		}
		return header
	# end

	def _get_data_thread(self, index=0, end=0):
		""" 线程处理 """
		url = self.config['base_url']
		header = self._get_header_v1()

		more = True
		fail = forbidden = reset = error414 = 0

		while more:
			print '\n no.' + str(index)
			params = self._get_params_v1(index)
			response = self.simple_request_v1(url, header, params)
			print '\t\t status: ' + str(response.status_code)
			if response.status_code == 200:
				util.output(self.config['requests_dir'], index, response.text)
				more = self._check_more_v1(response.text)
				print '\t\t\t has_more: ' + str(more)
				if more is False and fail < 10:
					more = True
					fail += 1
				else:
					fail = forbidden = error414 = 0
					index += 1
					if index > end : break
			elif response.status_code == 403:
				forbidden += 1
				if forbidden > 10:
					header = self._get_header_v1()
					forbidden = 0
					reset += 1
				if reset > 10 : break
			elif response.status_code == 414:
				error414 += 1
				if error414 > 10 : break
			else:
				if fail > 10 : break
				fail += 1
				print '\n\t\t something wrong, fail ' + str(fail) + '\n\n'
			# end if-elif-else
		# end while
		print '\n\n\t\t done!!! \n\n'
	# end

	def simple_request_v1(self, url, header, params):
		""" 发送一个请求 """
		print 'simple_request_v1: ' + str(params)
		if self.config.has_key('type') and self.config['type'] == 'post':
			response = requests.post(url, data=params, headers=header)
		else:
			response = requests.get(url, params=params, headers=header)
		return response
	# end

	def simple_request_with_header(self, url, params):
		""" 简单的请求，自带header """
		print 'simple_request_with_header: ' + str(params)
		header = self._get_header_v1(0)
		print header
		if self.config.has_key('type') and self.config['type'] == 'post':
			response = requests.post(url, data=params, headers=header)
		else:
			response = requests.get(url, params=params, headers=header)
		print response.status_code
		return response
	# end

	def get_data_v1(self, worker=10):
		""" 得到总页数，开10个线程请求 """
		total = self._get_total_page_v1()
		part = int(math.floor(total/worker))
		if part < 1:
			return
		try:
			callback = self._get_data_thread
			thread_list = list()
			for x in range(0,worker):
				arguments = (x*part+1, (x+1)*part)
				if x == 9:
					arguments = (x*part+1, total)
				item = threading.Thread(target=callback, args=arguments)
				thread_list.append(item)
		except Exception as e:
			print "Error: unable to start thread"
			raise
		print 'start thread'
		for item in thread_list:
			item.start()
	# end

	def _before_loop_file_v1(self):
		pass
	# end _before_loop_file_v1

	def _get_loop_data_v1(self, read_data):
		pass
	# end _get_loop_data_v1

	def _loop_item_v1(self, item):
		pass
	# end _loop_item_v1

	def _after_loop_file_v1(self):
		pass
	# end _after_loop_file_v1

	def extract_v1(self):
		""" extract 升级第一版 """
		print '\n in extract_v1 \n'
		files = util.get_dir_list(self.config['requests_dir'])
		if len(files) < 1:
			return
		if files[0].endswith('.txt'):
			files.sort(key=lambda x:int(x[:-4]))
		elif files[0].endswith('.json'):
			files.sort(key=lambda x:int(x[:-5]))
		self._before_loop_file_v1()
		for file in files:
			print '\n' + file + '\n'
			f = open(self.config['requests_dir'] + '/' + file)
			read_data = f.readlines()
			f.close()
			del f
			data = self._get_loop_data_v1(read_data)
			del read_data
			if len(data) < 1:
				continue
			for item in data:
				self._loop_item_v1(item)
			# end for item
		self._after_loop_file_v1()
		# end for file
	# end extract_v1

##############################################################################
##############################################################################
##############################################################################

	def get_data_v2(self, url=""):
		""" 单线程获取数据，适用于无法获得总页数的例子 """
		header = self._get_header_v1()
		if url == "":
			url = self.config['base_url']

		more = True
		fail = forbidden = reset = error414 = 0
		index = 1

		while more:
			print '\n no.' + str(index)
			params = self._get_params_v1(index)
			response = self.simple_request_v1(url, header, params)
			print '\t\t status: ' + str(response.status_code)
			if response.status_code == 200:
				util.output(self.config['requests_dir'], index, response.text)
				more = self._check_more_v1(response.text)
				print '\t\t\t has_more: ' + str(more)
				if fail > 10 : break
				if more is False:
					fail += 1
				else:
					fail = forbidden = error414 = 0
					index += 1
			elif response.status_code == 403:
				if reset > 10 : break
				forbidden += 1
				if forbidden > 10:
					header = self._get_header_v1()
					forbidden = 0
					reset += 1
			elif response.status_code == 414:
				if error414 > 10 : break
				error414 += 1
			else:
				if fail > 10 : break
				util.output(self.config['dump_dir'], 'error', response.text)
				fail += 1
				print '\n\t\t something wrong, fail ' + str(fail) + '\n\n'
			# end if-elif-else
		# end while
		print '\n\n\t\t done!!! \n\n'
	# end get_data_v2

# end Spider

