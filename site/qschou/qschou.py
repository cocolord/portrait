# -*- coding: utf-8 -*-
__author__ = 'qingfengsheng'

import json
import time

from lib.spider import Spider

class Qschou(Spider):
	"""docstring for Qschou"""
	def __init__(self, path):
		super(Qschou, self).__init__(path)
		# self.arg = arg

	def _get_params(self, index, page):
		""" 拼接 url 请求参数 """
		if not hasattr(self, 'r_timestamp'):
			self.r_timestamp = ""
			self.r_id = ""
		return "?timestamp=" + str(self.r_timestamp)\
			+ "&_=" + str(self.r_id)
	# end _get_params

	def _check_more(self, text):
		""" 检查是否还有更多数据，记录下次请求的凭据
		@return Bool <True> 有
		@return Bool <False> 无
		"""
		data = json.loads(text)
		if data['timestamp'] != 'null':
			self.r_timestamp = data['timestamp']
			self.r_id = data['id']
			return True
		else:
			return False
	# end _check_more

	def _filter(self, text):
		""" 因数据而已，需要返回格式化后的文本数据 """
		data = json.loads(''.join(text))
		if len(data['data']) == 0:
			return ""
		output = ""
		for item in data['data']:
			timestamp = item['created']
			time_array = time.localtime(timestamp)
			date_array = time.strftime("%Y-%m-%d %H:%M:%S", time_array).split(' ')
			r_date = date_array[0]
			r_time = date_array[1]
			item_string = r_date + '\t' + r_time + '\t' + str(item['id']) + '\t' \
					 + item['title'][1]['text'] + '\n'
			print item_string
			output += item_string
		return output
	# end _filter

# end class


if __name__ == '__main__':
	qschou = Qschou('config.ini')
	qschou.get_data()
	qschou.extract()