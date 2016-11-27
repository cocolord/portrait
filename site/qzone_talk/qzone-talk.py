# -*- coding: utf-8 -*-
__author__ = 'qingfengsheng'

import json

from lib.spider import Spider

class QzoneTalk(Spider):
	def __init__(self, path):
		super(QzoneTalk, self).__init__(path)
		print '\n in QzoneTalk __init__'
	# end __init__

	def _get_params(self, index, page):
		print '\n in QzoneTalk _get_params. \n'
		params = '?g_tk=' + '1013386782&' \
			+ 'hostuin=' + str(self.config['qq']) + '&res_type=2&'\
			+ 'res_attach=att%3Dback%255Fserver%255Finfo%253D'\
			+ 'offset%25253D' + str(index) + '%252526'\
			+ 'total%25253D' + '10' + '%252526'\
			+ 'basetime%25253D' + '1478769653' + '%252526'\
			+ 'feedsource%25253D' + '0' + '%2526'\
			+ 'lastrefreshtime%253D' + '1479901944' + '%2526'\
			+ 'lastseparatortime%253D' + '0' + '%2526'\
			+ 'loadcount%253D' + str(page) + '%26'\
			+ 'tl%3D' + '1478769653' + '&refresh_type=2&format=json'\
			+ 'sid=' + 'fw+1hiSDMLklIO7Q463NP55FrT78S321RSx7ae3fdf10201=='
		return params
	# end _get_params

	def _check_more(self, text):
		if text.find('"code":0,') == -1:
			return False
		if text.find('"hasmore":1') > 0:
			return True
		else:
			return False
	# end _check_more

	def _filter(self, text):
		text = ''.join(text).lstrip('_Callback(').rstrip(');')
		data = json.loads(text)
		output = ""
		if not data['data'].has_key('vFeeds'):
			print '\n\t no data'
			return ''
		for item in data['data']['vFeeds']:
			print item['id']['cellid']

			if not item.has_key('summary'):
				continue
			summary = item['summary']['summary'].replace('\n', '')
			output += summary + '\n'
		return output
	# end _filter

# end class


if __name__ == '__main__':
	QzoneTalk = QzoneTalk('config.ini')
	QzoneTalk.get_data()
	QzoneTalk.extract()