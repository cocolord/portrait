# -*- coding: utf-8 -*-
__author__ = 'qingfengsheng'

import json
import re

from pyquery import PyQuery as pq

from lib.spider import Spider
from lib.util import *

class HitLibrary(Spider):
	def __init__(self, path):
		super(HitLibrary, self).__init__(path)
		print '\n in HitLibrary __init__'
	# end __init__

	def _get_params(self, index, page):
		print '\n in HitLibrary _get_params. \n'
		params = '?method=process&seq=302&startDate=' + self.config['start_date']\
			+ '&endDate=' + self.config['end_date'] + '&displayCount=20'
		return params
	# end _get_params

	def _check_more(self, data):
		""" 修改 self.config['start_date'] 的值，更新请求时的参数
			不足20条，认定没有更多了
		"""
		text = ''.join(data)
		# '2014.11.27'
		pattern = re.compile(r'\d+\.+\d+\.+\d{2}')
		items = pattern.findall(text)
		if len(items) < 20:
			return False
		else:
			self.config['start_date'] = items[19]
			return True
	# end _check_more

	def _filter(self, data):
		""" 由于抓取参数的原因，存在重复数据 """
		text = ''.join(data)
		html = pq(text)
		table = html('table').eq(7)
		# 删除第一个子节点，thead，表格头
		table.children('tr').eq(0).remove()
		content = ''
		for tr in table.children('tr'):
			i = 0
			book = dict()
			handle = ''
			for td in tr.getchildren():
				info = td.findtext('font')
				if info is None : continue
				if i is 0 : handle += info + '-'
				if i is 1 : handle += info + ' '
				if i is 2 : handle += info
				if i is 3 : book['site'] = info
				if i is 4 : book['name'] = info
				if i is 5 : book['classify'] = info
				if i is 6 : book['isbn'] = info
				i += 1
			content += book['isbn'] + '\t' + book['name'] + '\t'\
				+ book['classify'] + '\t' + book['site'] + '\t'\
				+ handle + '\n'
		return content
	# end _filter

	def format_json(self):
		""" 去掉重复的数据，输出json数据
		{book: isbn	name 	classify	site	[handle]}
		"""
		data = read_file(self.config['dump_dir'] + '/total.txt')
		books_text = data.split('\n')
		books = dict()
		for book_str in books_text:
			if book_str is '' : continue
			i = 0
			book = dict()
			items = book_str.split('\t')
			print 'haha: ' + book_str + '\n'
			for item in items:
				if i is 0 : book['isbn'] = item
				if i is 1 : book['name'] = item
				if i is 2 : book['classify'] = item
				if i is 3 : book['site'] = item
				if i is 4 : handle = item
				i += 1
			book_id = book['isbn']
			if not books.has_key(book_id):
				books[book_id] = book
				books[book_id]['record'] = list()
			if handle not in books[book_id]['record']:
				books[book_id]['record'].append(handle)
		text = json.dumps(books, ensure_ascii=False)
		output(self.config['dump_dir'], 'total', text)
	# end format_json

# end class




if __name__ == '__main__':
	hit = HitLibrary('hit-library/config.ini')
	# hit.get_data()
	hit.extract()
	hit.format_json()