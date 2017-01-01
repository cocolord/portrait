# -*- coding: utf-8 -*-
__author__ = 'qingfengsheng'

from lib.spider import Spider
from lib.util import *

class Retweet(Spider):
	"""docstring for Retweet"""
	def __init__(self, path, tweet_id):
		"""
		@param <string> path
		@param <string> tweet_id
		"""
		super(Retweet, self).__init__(path)
		self.config['tweet_id'] = str(tweet_id)
		self.config['base_url'] = 'http://m.weibo.cn/api/statuses/repostTimeline'
		self.config['requests_dir'] = self.config['dump_dir'] + '/requests-retweet'
	# end

	def _get_total_page_v1(self):
		""" 得到需要请求的总次数 """
		url = self.config['base_url']
		header = self._get_header_v1()
		response = self.simple_request_v1(url, header, self._get_params_v1(1))
		try:
			data = json.loads(response.text)
		except Exception as e:
			print "Tip: please check cookie"
			print response.text
			raise
		print data['total_number']
		return data['total_number']
	# end

	def _get_params_v1(self, page):
		""" 在发送请求前做一些处理 主要是为了获取参数/数据 """
		return {
			'id': self.config['tweet_id'],
			'page': page
		}
	# end

	def _check_more_v1(self, text):
		""" 在请求成功返回后做一些处理 主要是为了检查是否还有更多 """
		if text.find('{"ok":1') > 0:
			return True
		return False
	# end

	def _before_loop_file_v1(self):
		self.retweet = list()
	# end _before_loop_file_v1

	def _get_loop_data_v1(self, read_data):
		data = json.loads(''.join(read_data))
		return data['data']
	# end _get_loop_data_v1

	def _loop_item_v1(self, item):
		weibo = dict()
		weibo['wbid'] = str(item['id'])
		weibo['uid'] = str(item['user']['id'])
		print weibo
		self.retweet.append(weibo)
	# end _loop_item_v1

	def _after_loop_file_v1(self):
		print json.dumps(self.retweet)
		# print json.dumps(sorted(self.retweet, key=lambda x:x['wbid']))
	# end _after_loop_file_v1

# end


if __name__ == '__main__':
	retweet = Retweet('config.ini', '4058078561880649')
	# retweet.get_data_v1()
	retweet.extract_v1()
