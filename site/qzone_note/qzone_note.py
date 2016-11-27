# -*- coding: utf-8 -*-
__author__ = 'qingfengsheng'

import json

from lib.spider import Spider

class QzoneNote(Spider):
	def __init__(self, path):
		super(QzoneNote, self).__init__(path)
		print '\n in QzoneNote __init__'
	# end __init__

	def _get_params(self, index, page):
		print '\n in QzoneNote _get_params. \n'
		params = '?g_tk=' + '1013386782' + '&res_attach=att%3D'\
			+ 'offset%253D' + str(index) + '%2526%26'\
			+ 'tl%3D' + '1401551356'+ '&format=json&list_type=msg&'\
			+ 'action=0&res_uin=' + str(self.config['qq']) + '&count=' + '10'\
			+ '&sid=' + '1hiSDMLklIO7Q463NP55FrT78S321RSx7ae3fdf10201=='
		return params
	# end _get_params

	def _check_more(self, text):
		if text.find('"code":0,') == -1:
			return False
		if text.find('"has_more":1') > 0:
			return True
		else:
			return False
	# end _check_more

	def _filter(self, text):
		data = json.loads(''.join(text))
		output = ""
		if not data.has_key('data'):
			print '\n\t no data'
			return ''
		for item in data['data']['vFeeds']:
			print item['id']['cellid']

			if not item.has_key('summary'):
				continue
			summary = item['summary']['summary'].replace('\n', '')
			# 去掉广告
			if summary.find('业务') > 0 or summary.find('Qq') > 0:
				continue
			# print summary + '\n'
			output += summary + '\n'
		return output
	# end _filter

# end class


if __name__ == '__main__':
	QzoneNote = QzoneNote('config.ini')
	QzoneNote.get_data()
	QzoneNote.extract()