# -*- coding: utf-8 -*-
__author__ = 'qingfengsheng'

import json

from lib.spider import Spider

class Weibo(Spider):
	def __init__(self, path):
		super(Weibo, self).__init__(path)
		print '\n in Weibo __init__'
		self.config['base_url'] = "http://m.weibo.cn/page/json?containerid=100505"\
			+ str(self.config['uid']) + "_-_WEIBO_SECOND_PROFILE_WEIBO&page="
	# end __init__

	def _get_params(self, index, page):
		print '\n in Weibo _get_params. \n'
		return str(page)
	# end _get_params

	def _check_more(self, text):
		if text.find('{"mod_type":"mod\/empty"') > 0:
			return False
		else:
			return True
	# end _check_more

	def _filter(self, text):
		data = json.loads(''.join(text))
		output = ""
		if data['cards'][0]['mod_type'] == "mod/empty":
			print '\n\t no data'
			return ''
		for item in data['cards'][0]['card_group']:
			print item['mblog']['id']
			if not item['mblog'].has_key('text'):
				continue
			summary = item['mblog']['text'].replace('\n', '')
			# print summary + '\n'
			output += summary + '\n'
		return output
	# end _filter

# end class


if __name__ == '__main__':
	weibo = Weibo('weibo/config.ini')
	weibo.get_data()
	weibo.extract()
