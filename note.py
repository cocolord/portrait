# -*- coding: utf-8 -*-
__author__ = 'qingfengsheng'

import json

from lib.spider import Spider

class Note(Spider):
	def __init__(self, path):
		super(Note, self).__init__(path)
		print '\n in Note __init__'
	# end __init__

	def _get_params(self, index, page):
		print '\n in Note _get_params. \n'
		params = '?g_tk=' + '1795135099' + '&res_attach=att%3D'\
			+ 'offset%253D' + str(index) + '%2526%26'\
			+ 'tl%3D' + '1472132755'+ '&format=json&list_type=msg&'\
			+ 'action=0&res_uin=' + str(self.config['qq']) + '&count=' + '10'\
			+ '&sid=' + 'hDT6jTad4qEa4nNBdilWxTJsQr9KnbRA347041050201=='
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

if __name__ == '__main__':
	note = Note('note/config.ini')
	# note.get_data()
	note.extract()