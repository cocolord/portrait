# -*- coding: utf-8 -*-
__author__ = 'qingfengsheng'

import json

from lib.spider import Spider

class Talk(Spider):
	def __init__(self, path):
		super(Talk, self).__init__(path)
		print '\n in Talk __init__'
	# end __init__

	def _get_params(self, index, page):
		print '\n in Talk _get_params. \n'
		params = '?g_tk=' + '1795135099&' \
			+ 'hostuin=' + str(self.config['qq']) + '&res_type=2&'\
			+ 'res_attach=att%3Dback%255Fserver%255Finfo%253D'\
			+ 'offset%25253D' + str(index) + '%252526'\
			+ 'total%25253D' + '10' + '%252526'\
			+ 'basetime%25253D' + '1454249267' + '%252526'\
			+ 'feedsource%25253D' + '0' + '%2526'\
			+ 'lastrefreshtime%253D' + '1479371528' + '%2526'\
			+ 'lastseparatortime%253D' + '0' + '%2526'\
			+ 'loadcount%253D' + str(page) + '%26'\
			+ 'tl%3D' + '1454249267' + '&refresh_type=2&format=json'\
			+ 'sid=' + 'hDT6jTad4qEa4nNBdilWxTJsQr9KnbRA347041050201=='
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
		if not data.has_key('data'):
			print '\n\t no data'
			return ''
		for item in data['data']['vFeeds']:
			print item['id']['cellid']

			if not item.has_key('summary'):
				continue
			summary = item['summary']['summary'].replace('\n', '')
			# print summary + '\n'
			output += summary + '\n'
		return output
	# end _filter

if __name__ == '__main__':
	talk = Talk('talk/config.ini')
	# talk.get_data()
	talk.extract()