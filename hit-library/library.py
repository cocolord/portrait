# -*- coding: utf-8 -*-
__author__ = 'qingfengsheng'

import json
import sys
sys.path.append('..')

from lib.util import *

class Library(object):
	"""docstring for Library"""
	def __init__(self, path):
		""" 读取配置文件，读取json数据 """
		self.config = init(path)
		self.books = json.loads(read_file(self.config['filter_file']))
	# end __init__

	def echo_books(self):
		""" 输出所有书籍的信息
		classify	book_name
		"""
		print len(self.books)

# end class



if __name__ == '__main__':
	lib = Library('config.ini')
	lib.echo_books()