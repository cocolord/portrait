# -*- coding: utf-8 -*-
__author__ = 'qingfengsheng'

import json

from lib.spider import Spider

class QzoneTalk(Spider):
	def __init__(self, path):
		super(QzoneTalk, self).__init__(path)
		self.response = ""
		print '\n in QzoneTalk __init__'
	# end __init__

	def _get_params(self, index, page):
		print '\n in QzoneTalk _get_params. \n'
		params = '?g_tk=' + '569917145&' \
			+ 'hostuin=' + str(self.config['qq']) + '&res_type=2&'\
			+ 'res_attach=att%3Dback%255Fserver%255Finfo%253D'\
			+ 'offset%25253D' + str(index) + '%252526'\
			+ 'total%25253D' + '10' + '%252526'\
			+ 'basetime%25253D' + '1454249267' + '%252526'\
			+ 'feedsource%25253D' + '0' + '%2526'\
			+ 'lastrefreshtime%253D' + '1480337034' + '%2526'\
			+ 'lastseparatortime%253D' + '0' + '%2526'\
			+ 'loadcount%253D' + str(page) + '%26'\
			+ 'tl%3D' + '1454249267' + '&refresh_type=2&format=json'\
			+ 'sid=' + '/udMhDcECD3tVZMrUfcpvjJsQr9KnbRA347041050201=='
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

#########################################################################
#########################################################################
#########################################################################

	# def _get_params(self, index, page):
	# 	print '\n in qzonetalk _get_params. \n'
	# 	res_attach = ""
	# 	if self.response != "":
	# 		self.response = self.response.replace('=', '%3D')
	# 		self.response = self.response.replace('&', '%26')
	# 		res_attach = "&res_attach=" + self.response
	# 	params = '?g_tk=' + '569917145' + res_attach + '&format=json&'\
	# 		+ 'list_type=shuoshuo&'\
	# 		+ 'action=0&res_uin=' + str(self.config['qq']) + '&count=10&'\
	# 		+ 'sid=' + '%2FudMhDcECD3tVZMrUfcpvjJsQr9KnbRA347041050201%3D%3D'
	# 	# att%3D10%26tl%3D
	# 	print params
	# 	return params

	# def _check_more(self, text):
	# 	data = json.loads(text)
	# 	if data['data']['attach_info']:
	# 		self.response = data['data']['attach_info']
	# 	if data['data']['has_more'] == 1:
	# 		return True
	# 	else:
	# 		return False

	# def _filter(self, text):
	# 	data = json.loads(''.join(text))
	# 	output = ""
	# 	if not data['data'].has_key('vFeeds'):
	# 		print '\n\t no data'
	# 		return ''
	# 	for item in data['data']['vFeeds']:
	# 		print item['id']['cellid']

	# 		if not item.has_key('summary'):
	# 			continue
	# 		summary = item['summary']['summary'].replace('\n', '')
	# 		output += summary + '\n'
	# 	return output

# end class


if __name__ == '__main__':
	QzoneTalk = QzoneTalk('config.ini')
	QzoneTalk.get_data()
	QzoneTalk.extract()