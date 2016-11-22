# -*- coding: utf-8 -*-
__author__ = 'qingfengsheng'

import requests

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

		while more:
			print '\n no.' + str(page)
			if self.config.has_key('cookie'):
				cookie = {"Cookie": self.config['cookie']}
			else:
				cookie = {"Cookie": ""}
			params = self._get_params(index, page)
			if self.config.has_key('type') and self.config['type'] == 'post':
				url = self.config['base_url']
				response = requests.post(url, data=params, cookies=cookie)
			else:
				url = self.config['base_url'] + params
				response = requests.get(url, cookies=cookie)
			print '\t\t status: ' + str(response.status_code)
			if response.status_code == 200:
				more = self._check_more(response.text)
				print '\t\t\t has_more: ' + str(more)
				util.output(self.config['dump_dir'], page, response.text)
				if more is False:
					if fail < 10:
						print '\n\tfail: ' + str(fail) + '\ttry again'
						more = True
						fail += 1
				else:
					page += 1
					index += 10
			else:
				print '\n\t\t something wrong\n\n'
				if fail > 10:
					break
				fail += 1
			print '\n'
	# end get_data

	def extract(self):
		""" 提取有效数据 """
		print '\n\t in extract'
		files = util.get_dir_list(self.config['dump_dir'])
		files.sort(key=lambda x:int(x[:-4]))
		content = ""
		for file in files:
			path = self.config['dump_dir'] + '/' + file
			f = open(path)
			text = f.readlines()
			f.close()
			print path
			# self._filter(text)
			content += self._filter(text)
		util.output(self.config['dump_dir'] + '-filter', 'total', content)
	# end extract


# end Spider

